import dabo
import dabo.dConstants as k
from dabo.db.dCursorMixin import dCursorMixin
from dabo.dLocalize import _
import dabo.dException as dException
import dabo.common
import types

class dBizobj(dabo.common.dObject):
	""" The middle tier, where the business logic resides.
	"""
	# Class to instantiate for the cursor object
	dCursorMixinClass = dCursorMixin

	# Versioning...
	_version = "0.1.0"
	
	# Need to set this here
	useFieldProps = False

	# Hack so that I can test until the app can return cursorsClasses, etc.
	TESTING = False
	

	def __init__(self, conn, testHack=TESTING):
		""" User code should override beforeInit() and/or afterInit() instead.
		"""
		self.__cursors = {}		# Collection of cursor objects. MUST be defined first.
		self.__currentCursorKey = None
		self._conn = conn
		self.__params = ()		# tuple of params to be merged with the sql in the cursor
		self.__children = []		# Collection of child bizobjs
		self._baseClass = dBizobj
		self.__areThereAnyChanges = False	# Used by the isChanged() method.
		# Next two are used by the scan() method.
		self.__scanRestorePosition = True	
		self.__scanReverse = False
		self.useFieldProps = True		# Do we look to getFieldVal for values?
		# Used by the LinkField property
		self._linkField = ""
		self._parentLinkField = ""
		# Used the the addChildByRelationDict() method to eliminate infinite loops
		self.__relationDictSet = False

		dBizobj.doDefault()		
		##########################################
		### referential integrity stuff ####
		##########################################
		### Possible values for each type (not all are relevant for each action):
		### IGNORE - don't worry about the presence of child records
		### RESTRICT - don't allow action if there are child records
		### CASCADE - changes to the parent are cascaded to the children
		self.deleteChildLogic = k.REFINTEG_CASCADE       # child records will be deleted
		self.updateChildLogic = k.REFINTEG_IGNORE    # parent keys can be changed w/o affecting children
		self.insertChildLogic = k.REFINTEG_IGNORE        # child records can be inserted even if no parent record exists.
		##########################################
		
		self.beforeInit()
		
		# Dictionary holding any default values to apply when a new record is created
		# (should be made into a property - do we have a name/value editor for the propsheet?)
		self.defaultValues = {}
		
		if self._conn:
			if testHack:
				import MySQLdb
				self.dbapiCursorClass = MySQLdb.cursors.DictCursor
			else:
				# Base cursor class : the cursor class from the db api
				self.dbapiCursorClass = self._conn.getDictCursorClass()
		
			# If there are any problems in the createCursor process, an
			# exception will be raised in that method.
			self.createCursor()

		self.afterInit()
		
		
	def beforeInit(self):
		""" Hook for subclasses.
		"""
		pass
	
	
	def afterInit(self):
		""" Hook for subclasses.
		"""
		pass
		

	def __getattr__(self, att):
		"""
		Allows for directly accessing the field values of the cursor without having
		to use self.getFieldVal(fld). If there is a field whose name is the same as 
		a built-in attribute of this object, the built-in value will always be returned.
		If there is no object attribute named 'att', and no field in the cursor by that
		name, an AttributeError is raised.
		"""
		if self.useFieldProps:
			try:
				ret = self.getFieldVal(att)
			except (dException.dException, dException.NoRecordsException):
				ret = None
			if ret is None:
				raise AttributeError, " '%s' object has no attribute '%s' " % (self.__class__.__name__, att)
			return ret


	def __setattr__(self, att, val):
		""" 
		Allows for directly setting field values as if they were attributes of the
		bizobj, rather than calling setFieldVal() for each field. If there is a field in
		the cursor with the same name as a built-in attribute of this object, the
		cursor field will be affected, not the built-in attribute.
		"""
		isFld = False
		if att != '_dBizobj__cursors' and self.__cursors is not {}:
			try:
				isFld = self.setFieldVal(att, val)
			except:
				isFld = None
		if not isFld:
			super(dBizobj, self).__setattr__(att, val)


	def createCursor(self, key=None):
		""" Create the cursor that this bizobj will be using for data, and store it
		in the dictionary for cursors, with the passed value of 'key' as its dict key. 
		For independent bizobjs, that key will be None.
		
		Subclasses should override beforeCreateCursor() and/or afterCreateCursor()
		instead of overriding this method, if possible. Returning any non-empty value
		from beforeCreateCursor() will prevent the rest of this method from
		executing.
		"""
		errMsg = self.beforeCreateCursor()
		if errMsg:
			raise dException.dException, errMsg
			
		cursorClass = self._getCursorClass(self.dCursorMixinClass,
				self.dbapiCursorClass)
		
		if key is None:
			key = self.__currentCursorKey
		
		if self.TESTING:
			self.__cursors[key] = self._conn.cursor(cursorclass=cursorClass)
		else:
			self.__cursors[key] = self._conn.getCursor(cursorClass)

		crs = self.__cursors[key]
		crs.setSQL(self.SQL)
		crs.KeyField = self.KeyField
		crs.Table = self.DataSource
		crs.AutoPopulatePK = self.AutoPopulatePK
		crs.BackendObject = self._conn.BackendObject
		if self.RequeryOnLoad:
			crs.requery()
		self.afterCreateCursor(crs)


	def _getCursorClass(self, main, secondary):
		class cursorMix(main, secondary):
			superMixin = main
			superCursor = secondary
			def __init__(self, *args, **kwargs):
				if hasattr(main, "__init__"):
					apply(main.__init__,(self,) + args, kwargs)
				if hasattr(secondary, "__init__"):
					apply(secondary.__init__,(self,) + args, kwargs)
		return  cursorMix


	def first(self):
		""" Move to the first record of the data set.
		
		Any child bizobjs will be requeried to reflect the new parent record. If 
		there are no records in the data set, an exception will be raised.
		"""
		errMsg = self.beforeFirst()
		if not errMsg:
			errMsg = self.beforePointerMove()
		if errMsg:
			raise dException.dException, errMsg

		self.Cursor.first()
		self.requeryAllChildren()

		self.afterPointerMove()
		self.afterFirst()


	def prior(self):
		""" Move to the prior record of the data set.
		
		Any child bizobjs will be requeried to reflect the new parent record. If 
		there are no records in the data set, an exception will be raised.
		"""
		errMsg = self.beforePrior()
		if not errMsg:
			errMsg = self.beforePointerMove()
		if errMsg:
			raise dException.dException, errMsg

		self.Cursor.prior()
		self.requeryAllChildren()

		self.afterPointerMove()
		self.afterPrior()


	def next(self):
		""" Move to the next record of the data set.
		
		Any child bizobjs will be requeried to reflect the new parent record. If 
		there are no records in the data set, an exception will be raised.
		"""
		errMsg = self.beforeNext()
		if not errMsg:
			errMsg = self.beforePointerMove()
		if errMsg:
			raise dException.dException, errMsg

		self.Cursor.next()
		self.requeryAllChildren()
		
		self.afterPointerMove()
		self.afterNext


	def last(self):
		""" Move to the last record of the data set.
		
		Any child bizobjs will be requeried to reflect the new parent record. If 
		there are no records in the data set, an exception will be raised.
		"""
		errMsg = self.beforeLast()
		if not errMsg:
			errMsg = self.beforePointerMove()
		if errMsg:
			raise dException.dException, errMsg

		self.Cursor.last()
		self.requeryAllChildren()

		self.afterPointerMove()
		self.afterLast()


	def saveAll(self, startTransaction=False, topLevel=True):
		""" Iterates through all the records of the bizobj, and calls save()
		for any record that has pending changes.
		"""
		if startTransaction:
			# Tell the cursor to issue a BEGIN TRANSACTION command
			self.Cursor.beginTransaction()
		
		try:
			self.scan(self._saveRowIfChanged)
		except dException, e:
			if startTransaction:
				self.Cursor.rollbackTransaction()
			raise dException, e
		
		if startTransaction:
			self.Cursor.commitTransaction()
			
	
	def _saveRowIfChanged(self):
		""" Meant to be called as part of a scan loop. That means that we can
		assume that the current record is the one we want to act on. Also, we
		can pass False for the two parameters, since they will have already been
		accounted for in the calling method.
		"""
		if self.isChanged():
			self.save(startTransaction=False, topLevel=False)
			

	def save(self, startTransaction=False, topLevel=True):
		""" Save any changes that have been made in the data set.
		
		If the save is successful, the save() of all child bizobjs will be
		called as well. 
		"""
		errMsg = self.beforeSave()
		if errMsg:
			raise dException.dException, errMsg
		
		if self.KeyField is None:
			raise dException.dException, "No key field defined for table: " + self.DataSource

		# Validate any changes to the data. If there is data that fails
		# validation, an Exception will be raised.
		self._validate()
		
		# See if we are saving a newly added record, or mods to an existing record.
		isAdding = self.Cursor.isAdding()
		if startTransaction:
			# Tell the cursor to issue a BEGIN TRANSACTION command
			self.Cursor.beginTransaction()

		# OK, this actually does the saving to the database
		try:
			self.Cursor.save()
			if isAdding:
				# Call the hook method for saving new records.
				self.onSaveNew()

			# Iterate through the child bizobjs, telling them to save themselves.
			for child in self.__children:
				# No need to start another transaction. And since this is a child bizobj, 
				# we need to save all rows that have changed.
				child.saveAll(startTransaction=False, topLevel=False)

			# Finish the transaction, and requery the children if needed.
			if startTransaction:
				self.Cursor.commitTransaction()
			if topLevel and self.RequeryChildOnSave:
				self.requeryAllChildren()

			self.setMemento()

		except dException.NoRecordsException, e:
			# Nothing to roll back; just throw it back for the form to display
			raise dException.NoRecordsException, e
			
		except dException.dException, e:
			# Something failed; reset things.
			if startTransaction:
				self.Cursor.rollbackTransaction()
			# Pass the exception to the UI
			raise dException.dException, e

		# Some backends (Firebird particularly) need to be told to write 
		# their changes even if no explicit transaction was started.
		self.Cursor.flush()
		
		# Two hook methods: one specific to Save(), and one which is called after any change
		# to the data (either save() or delete()).
		self.afterChange()
		self.afterSave()


	def cancelAll(self):
		""" Iterates through all the records, canceling each in turn. """
		self.scan(self.cancel)
		
		
	def cancel(self):
		""" Cancel any changes to the current record, reverting the fields
		back to their original values.
		"""
		errMsg = self.beforeCancel()
		if not errMsg:
			errMsg = self.beforePointerMove()
		if errMsg:
			raise dException.dException, errMsg

		# Tell the cursor to cancel any changes
		self.Cursor.cancel()
		# Tell each child to cancel themselves
		for child in self.__children:
			child.cancelAll()
			child.requery()

		self.setMemento()
		self.afterCancel()


	def delete(self, startTransaction=False):
		""" Delete the current row of the data set.
		"""
		errMsg = self.beforeDelete()
		if not errMsg:
			errMsg = self.beforePointerMove()
		if errMsg:
			raise dException.dException, errMsg
		
		if startTransaction:
			self.Cursor.beginTransaction()

		if self.KeyField is None:
			raise dException.dException, "No key field defined for table: " + self.DataSource

		if self.deleteChildLogic == k.REFINTEG_RESTRICT:
			# See if there are any child records
			for child in self.__children:
				if child.RowCount > 0:
					raise dException.dException, _("Deletion prohibited - there are related child records.")

		self.Cursor.delete()
		if self.RowCount == 0:
			# Hook method for handling the deletion of the last record in the cursor.
			self.onDeleteLastRecord()
		# Now cycle through any child bizobjs and fire their cancel() methods. This will
		# ensure that any changed data they may have is reverted. They are then requeried to
		# populate them with data for the current record in this bizobj.
		for child in self.__children:
			if self.deleteChildLogic == k.REFINTEG_CASCADE:
				child.deleteAll(startTransaction=False)
			else:
				child.cancelAll()
				child.requery()
				
		if startTransaction:
			self.Cursor.commitTransaction()
			
		# Some backends (Firebird particularly) need to be told to write 
		# their changes even if no explicit transaction was started.
		self.Cursor.flush()
		
		self.afterPointerMove()
		self.afterChange()
		self.afterDelete()


	def deleteAll(self, startTransaction=False):
		""" Delete all rows in the data set.
		"""
		while self.RowCount > 0:
			self.first()
			ret = self.delete(startTransaction)
	
	
	def getChangedRecordNumbers(self):
		""" Returns a list of record numbers for which isChanged()
		returns True. The changes may therefore not be in the record 
		itself, but in a dependent child record.
		"""
		self.__changedRecordNumbers = []
		self.scan(self._listChangedRecordNumbers)
		return self.__changedRecordNumbers
	
	
	def _listChangedRecordNumbers(self):
		""" Called from a scan loop. If the current record is changed, 
		append the RowNumber to the list.
		"""
		if self.isChanged():
			self.__changedRecordNumbers.append(self.RowNumber)
	
	
	def getRecordStatus(self, rownum=None):
		""" Returns a dictionary containing an element for each changed 
		field in the specified record (or the current record if none is specified).
		The field name is the key for each element; the value is a 2-element
		tuple, with the first element being the original value, and the second 
		being the current value.
		"""
		if rownum is None:
			rownum = self.RowNumber
		return self.Cursor.getRecordStatus(rownum)


	def scan(self, func, *args, **kwargs):
		""" Iterates over all the records in the Cursor, and applies the passed
		function to each. If 'self.__scanRestorePosition' is True, the position of the current
		record in the recordset is restored after the iteration. If 'self.__scanReverse' is true, 
		the records are processed in reverse order.
		"""
		if self.RowCount <= 0:
			# Nothing to scan!
			return
			
		# Flag that the function can set to prematurely exit the scan
		self.exitScan = False
		if self.__scanRestorePosition:
			currRow = self.RowNumber
		try:
			if self.__scanReverse:
				recRange = range(self.RowCount-1, -1, -1)
			else:
				recRange = range(self.RowCount)
			for i in recRange:
				self._moveToRowNum(i)
				func(*args, **kwargs)
				if self.exitScan:
					break
		except dException, e:
			if self.__scanRestorePosition:
				self.RowNumber = currRow
			raise dException, e

		if self.__scanRestorePosition:
			try:	
				self.RowNumber = currRow
			except:
				# Perhaps the row was deleted; at any rate, leave the pointer
				# at the end of the data set
				row = self.RowCount  - 1
				if row >= 0:
					self.RowNumber = row
				


	def new(self):
		""" Create a new record and populate it with default values.
		 
		Default values are specified in the defaultValues dictionary. 
		"""
		errMsg = self.beforeNew()
		if not errMsg:
			errMsg = self.beforePointerMove()
		if errMsg:
			raise dException.dException, errMsg

		self.Cursor.new()
		# Hook method for things to do after a new record is created.
		self.onNew()

		# Update all child bizobjs
		self.requeryAllChildren()

		if self.NewChildOnNew:
			# Add records to all children set to have records created on a new parent record.
			for child in self.__children:
				if child.NewRecordOnNewParent:
					child.new()

		self.setMemento()
		self.afterPointerMove()
		self.afterNew()


	def setSQL(self, sql=None):
		""" Set the SQL query that will be executed upon requery().
		
		This allows you to manually override the sql executed by the cursor. If no
		sql is passed, the SQL will get set to the value returned by getSQL().
		"""
		if sql is None:
			# sql not passed; get it from the sql mixin:
			# Set the appropriate child filter on the link field
			self.setChildLinkFilter()

			self.SQL = self.getSQL()
		else:
			# sql passed; set it explicitly
			self.SQL = sql
		# propagate the SQL downward:
		self.Cursor.setSQL(self.SQL)


	def requery(self):
		""" Requery the data set.
		
		Refreshes the data set with the current values in the database, 
		given the current state of the filtering parameters.
		"""
		errMsg = self.beforeRequery()
		if errMsg:
			raise dException.dException, errMsg
		if self.KeyField is None:
			errMsg = "No Primary Key defined in the Bizobj for " + self.DataSource
			raise dException.MissingPKException, errMsg
		
		# If this is a dependent (child) bizobj, this will enforce the relation
		self.setChildLinkFilter()

		# Hook method for creating the param list
		params = self.getParams()
		
		# Record this in case we need to restore the record position
		try:
			currPK = self.getPK()
		except dException.NoRecordsException:
			currPK = None

		# run the requery
		self.Cursor.requery(params)

		if self.RestorePositionOnRequery:
			self._moveToPK(currPK)
				
		try:
			self.requeryAllChildren()
		except dException.NoRecordsException:
			pass
		self.setMemento()
		self.afterRequery()
	
	
	def setChildLinkFilter(self):
		""" If this is a child bizobj, its record set is dependent on its parent's 
		current PK value. This will add 
		"""
		if self.DataSource and self.LinkField:
			if self.ParentLinkField:
				# The link to the parent is something other than the PK
				val = self.escQuote(self.Parent.getFieldVal(self.ParentLinkField))
			else:
				val = self.escQuote(self.getParentPK())
			self.Cursor.setChildFilterClause(" %s.%s = %s " % (self.DataSource, 
					self.LinkField, val) )
					

	def sort(self, col, ord=None, caseSensitive=True):
		""" Sort the rows based on values in a specified column.
		
		Called when the data is to be sorted on a particular column
		in a particular order. All the checking on the parameters is done
		in the cursor. 
		"""
		self.Cursor.sort(col, ord, caseSensitive)


	def setParams(self, params):
		""" Set the query parameters for the cursor.
		
		Accepts a tuple that will be merged with the sql statement using the
		cursor's standard method for merging.
		"""
		self.__params = params


	def _validate(self):
		""" Internal method. User code should override validateRecord().
		
		_validate() is called by the save() routine before saving any data.
		If any data fails validation, an exception will be raised, and the
		save() will not be allowed to proceed.
		"""
		errMsg = ""
		if self.isChanged():
			# No need to validate if the data hasn't changed
			message = self.validateRecord()
			if message:
				errMsg += self.validateRecord()
		if errMsg:
			raise dException.BusinessRuleViolation, errMsg


	def validateRecord(self):
		""" Hook for subclass business rule validation code.
		
		This is the method that you should customize in your subclasses
		to create checks on the data entered by the user to be sure that it 
		conforms to your business rules. Your validation code should return 
		an error message that describes the reason why the data is not 
		valid; this message will be propagated back up to the UI where it can
		be displayed to the user so that they can correct the problem. 
		Example:

			if not myNonEmptyField:
				return "MyField must not be blank"

		It is assumed that we are on the correct record for testing before
		this method is called.
		"""
		pass


	def _moveToRowNum(self, rownum, updateChildren=True):
		""" For internal use only! Should never be called from a developer's code.
		It exists so that a bizobj can move through the records in its cursor
		*without* firing additional code.
		"""
		self.Cursor.moveToRowNum(rownum)
		if updateChildren:
			pk = self.getPK()
			for child in self.__children:
				# Let the child know the current dependent PK
				child.setCurrentParent(pk)


	def _moveToPK(self, pk, updateChildren=True):
		""" For internal use only! Should never be called from a developer's code.
		It exists so that a bizobj can move through the records in its cursor
		*without* firing additional code.
		"""
		self.Cursor.moveToPK(pk)
		if updateChildren:
			for child in self.__children:
				# Let the child know the current dependent PK
				child.setCurrentParent(pk)


	def seek(self, val, fld=None, caseSensitive=False, 
			near=False, runRequery=False):
		""" Search for a value in a field, and move the record pointer to the match.
		
		Used for searching of the bizobj's cursor for a particular value in a 
		particular field. Can be optionally case-sensitive.
		
		If 'near' is True, and no exact match is found in the cursor, the cursor's
		record pointer will be placed at the record whose value in that field
		is closest to the desired value without being greater than the requested 
		value.
		
		If runRequery is True, and the record pointer is moved, all child bizobjs
		will be requeried, and the afterPointerMove() hook method will fire.
		"""
		ret = self.Cursor.seek(val, fld, caseSensitive, near)
		if ret != -1:
			if runRequery:
				self.requeryAllChildren()
				self.afterPointerMove()
		return ret
	
	
	def isAnyChanged(self):
		""" Returns True if any record in the current record set has been 
		changed.
		"""
		self.__areThereAnyChanges = False
		self.scan(self._checkForChanges)
		return self.__areThereAnyChanges
	
	
	def _checkForChanges(self):
		""" Designed to be called from the scan iteration over the records
		for this bizobj. Once one changed record is found, set the scan's 
		exit flag, since we only need to know if anything has changed.
		"""
		if self.isChanged():
			self.__areThereAnyChanges = True
			self.exitScan = True


	def isChanged(self):
		""" Return True if data has changed in this bizobj and any children.
		
		By default, only the current record is checked. Call isAnyChanged() to
		check all records.
		"""
		ret = self.Cursor.isChanged(allRows = False)
		
		if not ret:
			# see if any child bizobjs have changed
			for child in self.__children:
				ret = child.isAnyChanged()
				if ret:
					break
		return ret


	def onDeleteLastRecord(self):
		""" Hook called when the last record has been deleted from the data set.
		"""
		pass


	def onSaveNew(self):
		""" Called after successfully saving a new record.
		"""
		# If this is a new parent record with a new auto-generated PK, pass it on
		# to the children before they save themselves.
		if self.AutoPopulatePK:
			pk = self.getPK()
			for child in self.__children:
				child.setParentFK(pk)
		# Call the custom hook method
		self.onSaveNewHook()


	def onSaveNewHook(self):
		""" Hook method called after successfully saving a new record.
		"""
		pass


	def onNew(self):
		""" Populate the record with any default values.
		
		User subclasses should leave this alone and instead override onNewHook(). 
		"""
		self.Cursor.setDefaults(self.defaultValues)
		
		if self.AutoPopulatePK:
			# Provide a temporary PK so that any linked children can be properly
			# identified until the record is saved and a permanent PK is obtained.
			self.Cursor.genTempAutoPK()
		
		# Fill in the link to the parent record
		if self.Parent and self.FillLinkFromParent and self.LinkField:
			self.setParentFK()

		# Call the custom hook method
		self.onNewHook()


	def onNewHook(self):
		""" Hook method called after the default values have been set in onNew(). 
		"""
		pass


	def setParentFK(self, val=None):
		""" Accepts and set the foreign key value linking to the parent table.
		"""
		if self.LinkField:
			if val is None:
				val = self.getParentPK()
			self.setFieldVal(self.LinkField, val)
	
	
	def setCurrentParent(self, val=None):
		""" Lets dependent child bizobjs know the current value of their parent
		record.
		"""
		if self.LinkField:
			if val is None:
				val = self.getParentPK()
			# Update the key value for the cursor
			self.__currentCursorKey = val
			# Make sure there is a cursor object for this key.
			self.setCurrentCursor()
	
	
	def setCurrentCursor(self):
		""" Sees if there is a cursor in the cursors dict with a key that matches
		the current parent key. If not, creates one.
		"""
		if not self.__cursors.has_key(self.__currentCursorKey):
			self.createCursor()
	
	
	def addChild(self, child):
		""" Add the passed child bizobj to this bizobj.
		
		During the creation of the form, child bizobjs are added by the parent.
		This stores the child reference here, and sets the reference to the 
		parent in the child. 
		"""
		if child not in self.__children:
			self.__children.append(child)
			child.Parent = self
	
	
	def addChildByRelationDict(self, dict, bizModule):
		""" Accepts a dictionary containing relationship information
		If any of the entries pertain to this bizobj, it will check to make 
		sure that the child bizobj is already added, or add it and set the 
		relationship if it isn't. It then passes the dict on to the child to
		allow the child to set up its relationships.
		
		Returns a list containing all added child bizobjs. The list will
		be empty if none were added.
		"""
		addedChildren = []
		if self.__relationDictSet:
			# already done this...
			return addedChildren
		self.__relationDictSet = True
		myRelations = [ dict[k] for k in dict.keys() 
				if dict[k]['parent'].lower() == self.DataSource.lower() ]
		if not myRelations:
			return addedChildren
		
		for relation in myRelations:
			# Each 'relation' is a dict with the following structure:
			# 'child': child table
			# 'childField': field in child table linked to parent
			# 'parent': parent table
			# 'parentField': field in parent table linked to child
			child = relation["child"]
			childField = relation["childField"]
			parent = relation["parent"]
			parentField = relation["parentField"]
			
			if self.getAncestorByDataSource(child):
				# The 'child' already exists as an ancestor of this bizobj. This can
				# happen in many-to-many relationships. We don't want to add it,
				# as this creates infinite loops.
				continue
				
			childBiz = self.getChildByDataSource(child)
			if not childBiz:
				childBizClass = bizModule.__dict__["Biz" + child.title()]
				childBiz = childBizClass(self._conn)
				self.addChild(childBiz)
				addedChildren.append(childBiz)
				childBiz.LinkField = childField
				if parentField != self.KeyField:
					childBiz.ParentLinkField = parentField
			# Now pass this on to the child
			addedGrandChildren = childBiz.addChildByRelationDict(dict, bizModule)
			for gc in addedGrandChildren:
				addedChildren.append(gc)
		return addedChildren
	
	
	def getAncestorByDataSource(self, ds):
		ret = None
		if self.Parent:
			if self.Parent.DataSource == ds:
				ret = self.Parent
			else:
				ret = self.Parent.getAncestorByDataSource(ds)
		return ret
	
	
	def requeryAllChildren(self):
		""" Requery each child bizobj's data set.
		
		Called to assure that all child bizobjs have had their data sets 
		refreshed to match the current master row. This will normally happen
		automatically when appropriate, but user code may call this as well
		if needed.
		"""
		if len(self.__children) == 0:
			return True
		
		errMsg = self.beforeChildRequery()
		if errMsg:
			raise dException.dException, errMsg

		pk = self.getPK()
		for child in self.__children:
			# Let the child know the current dependent PK
			child.setCurrentParent(pk)
			if not child.isChanged():
				child.requery()

		self.afterChildRequery()


	def getPK(self):
		""" Return the value of the PK field.
		"""
		if self.KeyField is None:
			raise dException.dException, "No key field defined for table: " + self.DataSource

		return self.Cursor.getFieldVal(self.KeyField)


	def getParentPK(self):
		""" Return the value of the parent bizobjs' PK field. 
		
		Alternatively, user code can just call self.Parent.getPK().
		"""
		try:
			return self.Parent.getPK()
		except dException.NoRecordsException:
			# The parent bizobj has no records
			return None


	def getFieldVal(self, fld):
		""" Return the value of the specified field in the current row. 
		"""
		if self.Cursor is not None:
			return self.Cursor.getFieldVal(fld)
		else:
			return None


	def setFieldVal(self, fld, val):
		""" Set the value of the specified field in the current row.
		"""
		if self.Cursor is not None:
			try:
				self.Cursor.setFieldVal(fld, val)
				return True
			except:
				return False
		else:
			return None


	def getDataSet(self):
		""" Return the full data set from the cursor. 
		
		Used by UI objects such as the grid for efficient reading of the data,
		and user code can do this as well if needed, but you'll need to keep 
		the bizobj notified of any row changes and field value changes manually.
		"""
		return self.Cursor.getDataSet()


	def getParams(self):
		""" Return the parameters to send to the cursor's execute method.
		
		This is the place to define the parameters to be used to modify
		the SQL statement used to produce the record set. If the cursor for
		this bizobj does not need parameters, leave this as is. Otherwise, 
		override this method to return a tuple to be passed to the cursor, where 
		it will be used to modify the query using standard printf syntax. 
		"""
		return self.__params


	def setMemento(self):
		""" Take a snapshot of the data in the cursor.
		
		Tell the cursor to take a snapshot of the current state of the 
		data. This snapshot will be used to determine what, if anything, has 
		changed later on. 
		
		User code should not normally call this method.
		"""
		self.Cursor.setMemento()


	def getChildren(self):
		""" Return a tuple of the child bizobjs.
		"""
		ret = []
		for child in self.__children:
			ret.append(child)
		return tuple(ret)
		
	
	def getChildByDataSource(self, dataSource):
		""" Return a reference to the child bizobj with the passed dataSource.
		"""
		ret = None
		for child in self.getChildren():
			if child.DataSource == dataSource:
				ret = child
				break
		return ret


	def escQuote(self, val):
		""" Escape special characters in SQL strings.

		Escapes any single quotes that could cause SQL syntax errors. Also 
		escapes backslashes, since they have special meaning in SQL parsing. 
		Finally, wraps the value in single quotes.
		"""
		return self.Cursor.escQuote(val)
	
	
	def formatDateTime(self, val):
		""" Wrap a date or date-time value in the format 
		required by the backend.
		"""
		return self.Cursor.formatDateTime(val)


	def getNonUpdateFields(self):
		return self.Cursor.getNonUpdateFields()
		
	def setNonUpdateFields(self, fldList=[]):
		self.Cursor.setNonUpdateFields(fldList)
		
		
	########## SQL Builder interface section ##############
	def addField(self, exp):
		return self.Cursor.addField(exp)
	def addFrom(self, exp):
		return self.Cursor.addFrom(exp)
	def addGroupBy(self, exp):
		return self.Cursor.addGroupBy(exp)
	def addOrderBy(self, exp):
		return self.Cursor.addOrderBy(exp)
	def addWhere(self, exp, comp="and"):
		return self.Cursor.addWhere(exp)
	def getSQL(self):
		return self.Cursor.getSQL()
	def setFieldClause(self, clause):
		return self.Cursor.setFieldClause(clause)
	def setFromClause(self, clause):
		return self.Cursor.setFromClause(clause)
	def setGroupByClause(self, clause):
		return self.Cursor.setGroupByClause(clause)
	def setLimitClause(self, clause):
		return self.Cursor.setLimitClause(clause)
	def setOrderByClause(self, clause):
		return self.Cursor.setOrderByClause(clause)
	def setWhereClause(self, clause):
		return self.Cursor.setWhereClause(clause)
	def prepareWhere(self, clause):
		return self.Cursor.prepareWhere(clause)
		




	########## Pre-hook interface section ##############
	def beforeNew(self): return ""
	def beforeDelete(self): return ""
	def beforeFirst(self): return ""
	def beforePrior(self): return ""
	def beforeNext(self): return ""
	def beforeLast(self): return ""
	def beforeSetRowNumber(self): return ""
	def beforePointerMove(self): return ""
	def beforeSave(self): return ""
	def beforeCancel(self): return ""
	def beforeRequery(self): return ""
	def beforeChildRequery(self): return ""
	def beforeCreateCursor(self): return ""
	########## Post-hook interface section ##############
	def afterNew(self): pass
	def afterDelete(self): pass
	def afterFirst(self): pass
	def afterPrior(self): pass
	def afterNext(self): pass
	def afterLast(self): pass
	def afterSetRowNumber(self): pass
	def afterPointerMove(self): pass
	def afterSave(self): pass
	def afterCancel(self): pass
	def afterRequery(self): pass
	def afterChildRequery(self): pass
	def afterChange(self): pass
	def afterCreateCursor(self, cursor): pass


	def _getCaption(self):
		try:
			return self._caption
		except AttributeError:
			return self.DataSource
	def _setCaption(self, val):
		self._caption = str(val)
	
	def _getDataSource(self):
		try: 
			return self._dataSource
		except AttributeError:
			return ""
	def _setDataSource(self, val):
		self._dataSource = str(val)
		
	def _getSQL(self):
		try:
			return self._SQL
		except AttributeError:
			return ""
	def _setSQL(self, val):
		self._SQL = str(val)
			
	def _getRequeryOnLoad(self):
		try:
			ret = self._requeryOnLoad
		except AttributeError:
			ret = False
		return ret
	def _setRequeryOnLoad(self, val):
		self._requeryOnLoad = bool(val)
		
	def _getParent(self):
		try:
			return self._parent
		except AttributeError:
			return None
	def _setParent(self, val):
		if isinstance(val, dBizobj):
			self._parent = val
		else:
			raise TypeError, "Parent must descend from dBizobj"
			
	def _getAutoPopulatePK(self):
		try:
			return self._autoPopulatePK
		except AttributeError:
			return True
	def _setAutoPopulatePK(self, val):
		self._autoPopulatePK = bool(val)
	
	def _getKeyField(self):
		try:
			return self._keyField
		except AttributeError:
			return ""
	def _setKeyField(self, val):
		self._keyField = val
	
	def _getLinkField(self):
		try:
			return self._linkField
		except AttributeError:
			return ""
	def _setLinkField(self, val):
		self._linkField = str(val)
		
	def _getParentLinkField(self):
		try:
			return self._parentLinkField
		except AttributeError:
			return ""
	def _setParentLinkField(self, val):
		self._parentLinkField = str(val)
		
	def _getRequeryChildOnSave(self):
		try:
			return self._requeryChildOnSave
		except AttributeError:
			return False
	def _setRequeryChildOnSave(self, val):
		self._requeryChildOnSave = bool(val)
		
	def _getNewRecordOnNewParent(self):
		try:
			return self._newRecordOnNewParent
		except AttributeError:
			return False
	def _setNewRecordOnNewParent(self, val):
		self._newRecordOnNewParent = bool(val)
		
	def _getNewChildOnNew(self):
		try:
			return self._newChildOnNew
		except AttributeError:
			return False
	def _setNewChildOnNew(self, val):
		self._newChildOnNew = bool(val)
					
	def _getFillLinkFromParent(self):
		try:
			return self._fillLinkFromParent
		except AttributeError:
			return False
	def _setFillLinkFromParent(self, val):
		self._fillLinkFromParent = bool(val)
		
	def _getRestorePositionOnRequery(self):
		try:
			return self._restorePositionOnRequery
		except AttributeError:
			return True
	def _setRestorePositionOnRequery(self, val):
		self._restorePositionOnRequery = bool(val)

	def _getCurrentCursor(self):
		return self.__cursors[self.__currentCursorKey]
	
	def _getRowCount(self):
		return self.Cursor.RowCount

	def _getRowNumber(self):
		return self.Cursor.RowNumber
	def _setRowNumber(self, rownum):
		errMsg = self.beforeSetRowNumber()
		if not errMsg:
			errMsg = self.beforePointerMove()
		if errMsg:
			raise dException.dException, errMsg
		self._moveToRowNum(rownum)
		self.requeryAllChildren()
		self.afterPointerMove()
		self.afterSetRowNumber()
	
	
	### -------------- Property Definitions ------------------  ##
	
	RowNumber = property(_getRowNumber, _setRowNumber, None, 
			_("The current position of the record pointer in the result set. (int)"))

	RowCount = property(_getRowCount, None, None, 
			_("The number of records in the cursor's data set. It will be -1 if the "
			"cursor hasn't run any successful queries yet. (int)"))

	Caption = property(_getCaption, _setCaption, None,
				_("The friendly title of the cursor, used in messages to the end user. (str)"))
	
	DataSource = property(_getDataSource, _setDataSource, None,
				_("The title of the cursor. Used in resolving DataSource references. (str)"))
	
	SQL = property(_getSQL, _setSQL, None, 
				_("SQL statement used to create the cursor\'s data. (str)"))
	
	RequeryOnLoad = property(_getRequeryOnLoad, _setRequeryOnLoad, None, 
				_("When true, the cursor object runs its query immediately. This "
				"is useful for lookup tables or fixed-size (small) tables. (bool)"))
	
	AutoPopulatePK = property(_getAutoPopulatePK, _setAutoPopulatePK, None, 
				_("Determines if we are using a table that auto-generates its PKs. (bool)"))

	Parent = property(_getParent, _setParent, None,
				_("Reference to the parent bizobj to this one. (dBizobj)"))

	KeyField = property(_getKeyField, _setKeyField, None,
				_("Name of field that is the PK. If multiple fields make up the key, "
				"separate the fields with commas. (str)"))
	
	LinkField = property(_getLinkField, _setLinkField, None,
				_("Name of the field that is the foreign key back to the parent. (str)"))
	
	ParentLinkField = property(_getParentLinkField, _setParentLinkField, None,
				_("Name of the field in the parent table that is used to determine child "
				"records. If empty, it is assumed that the parent's PK is used (str)"))
	
	RequeryChildOnSave = property(_getRequeryChildOnSave, _setRequeryChildOnSave, None,
				_("Do we requery child bizobjs after a Save()? (bool)"))
				
	NewChildOnNew = property(_getNewChildOnNew, _setNewChildOnNew, None, 
				_("Should new child records be added when a new parent record is added? (bool)"))
	
	NewRecordOnNewParent = property(_getNewRecordOnNewParent, _setNewRecordOnNewParent, None,
				_("If this bizobj\'s parent has NewChildOnNew==True, do we create a record here? (bool)"))

	FillLinkFromParent = property(_getFillLinkFromParent, _setFillLinkFromParent, None,
				_("In the onNew() method, do we fill in the linkField with the value returned "
				"by calling the parent bizobj\'s GetKeyValue() method? (bool)"))
				
	RestorePositionOnRequery = property(_getRestorePositionOnRequery, _setRestorePositionOnRequery, None,
				_("After a requery, do we try to restore the record position to the same PK?"))
				
	NonUpdateFields = property(getNonUpdateFields, setNonUpdateFields, None,
				_("Fields in the cursor to be ignored during updates"))
	
	Cursor = property(_getCurrentCursor, None, None, 
				_("Returns the reference to the currently active cursor object. Read-only."))
