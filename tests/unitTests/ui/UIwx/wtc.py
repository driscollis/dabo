"""
This is based on the one created by Robin Dunn for wxPython Phoenix.
"""
import unittest
import sys, os
import six

import dabo
from dabo.lib import getRandomUUID
import dabo.ui
dabo.ui.loadUI('wx')
import wx

#---------------------------------------------------------------------------

class WidgetTestCase(unittest.TestCase):
	"""
	A testcase that will create an app and frame for various widget test
	modules to use. They can inherit from this class to save some work. This
	is also good for test cases that just need to have an application object
	created.
	"""
	def setUp(self):
		self.app = dabo.dApp()
		self.app.setup()
		wx.Log.SetActiveTarget(wx.LogStderr())
		self.form = dabo.ui.dForm()

	def tearDown(self):
		def _cleanup():
			for tlw in wx.GetTopLevelWindows():
				if tlw:
					tlw.Destroy()
			wx.WakeUpIdle()
		# doesn't work with Dabo, crash without exception
		#wx.CallLater(50, _cleanup)
		self.app = None   
		del self.app


	# helper methods

	def setProperty(self, propertyInfo):
		"""setProperty(self, (object.property, val))"""
		exec("%s = %s" % propertyInfo)

	def mockUserInput(self, str_val, lose_focus=True):
		"""Assumes a 'self.txt' be present."""
		txt = self.txt
		txt._gotFocus()
		txt.SetValue(str_val)
		if lose_focus:
			txt._lostFocus()

	def myYield(self, eventsToProcess=wx.EVT_CATEGORY_ALL):
		"""
		Since the tests are usually run before MainLoop is called then we
		need to make our own EventLoop for Yield to actually do anything
		useful.
		"""
		evtLoop = self.app.GetTraits().CreateEventLoop()
		activator = wx.EventLoopActivator(evtLoop) # automatically restores the old one
		evtLoop.YieldFor(eventsToProcess)

	def myUpdate(self, window):
		"""
		Since Update() will not trigger paint events on Mac faster than
		1/30 of second we need to wait a little to ensure that there will
		actually be a paint event while we are yielding.
		"""
		if 'wxOSX' in wx.PlatformInfo:
			wx.MilliSleep(40)  # a little more than 1/30, just in case
		window.Update()

	def closeDialogs(self):
		"""
		Close dialogs by calling their EndModal method
		"""
		#self.myYield()
		for w in wx.GetTopLevelWindows():
			if isinstance(w, wx.Dialog):
				w.EndModal(wx.ID_CANCEL)

	def waitFor(self, milliseconds):
		intervals = milliseconds/100
		while intervals > 0:
			wx.MilliSleep(100)
			self.myYield()
			if hasattr(self, 'flag') and self.flag:
				break
			intervals -= 1

	def myExecfile(self, filename, ns):
		if not six.PY3:
			execfile(filename, ns)
		else:
			with open(filename, 'r') as f:
				source = f.read()
			exec(source, ns)

	def execSample(self, name):
		ns = Namespace()
		samplesDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../samples'))        
		self.myExecfile(os.path.join(samplesDir, name), ns.dict())
		return ns


#---------------------------------------------------------------------------


class WidgetTestCaseWithDB(unittest.TestCase):
	"""
	A testcase that will create an app and frame for various widget test
	modules to use. They can inherit from this class to save some work. This
	is also good for test cases that just need to have an application object
	created.

	This one also creates a database.
	"""
	def setUp(self):
		# We set up a test connection to an in-memory sqlite database, and then we
		# make a dBizobj against the test table, and then we create a dForm with some
		# dTextBox's to test the interaction.
		self.con = dabo.db.dConnection(DbType="SQLite", Database=":memory:")
		biz = self.biz = dabo.biz.dBizobj(self.con)
		uniqueName = getRandomUUID().replace("-", "")[-20:]
		self.temp_table_name = "unittest%s" % uniqueName
		self.temp_child_table_name = "ut_child%s" % uniqueName
		self.createSchema()
		biz.UserSQL = "select * from %s" % self.temp_table_name
		biz.KeyField = "pk"
		biz.DataSource = self.temp_table_name
		biz.requery()

		self.app = dabo.dApp()
		self.app.setup()
		wx.Log.SetActiveTarget(wx.LogStderr())
		self.form = dabo.ui.dForm()

		frm = self.frm = dabo.ui.dForm(Caption="test_dForm")
		frm.addObject(dabo.ui.dTextBox, DataSource=biz.DataSource, DataField="cField", RegID="cField")
		frm.addObject(dabo.ui.dTextBox, DataSource=biz.DataSource, DataField="nField", RegID="nField")
		frm.addObject(dabo.ui.dTextBox, DataSource=biz.DataSource, DataField="iField", RegID="iField")

		## connect the biz to the frm:
		frm.addBizobj(biz)

		## force the frm to get the first record:
		frm.first()
		frm.update(interval=0)  ## need to force the update here because it is delayed by default, which doesn't work for scripted tests.

	def tearDown(self):
		def _cleanup():
			for tlw in wx.GetTopLevelWindows():
				if tlw:
					tlw.Destroy()
			wx.WakeUpIdle()
		# doesn't work with Dabo, crash without exception
		#wx.CallLater(50, _cleanup)
		self.app = None   
		del self.app


	# helper methods

	def setProperty(self, propertyInfo):
		"""setProperty(self, (object.property, val))"""
		exec("%s = %s" % propertyInfo)

	def createSchema(self):
		biz = self.biz
		tableName = self.temp_table_name
		childTableName = self.temp_child_table_name
		biz._CurrentCursor.executescript("""
create table %(tableName)s (pk INTEGER PRIMARY KEY AUTOINCREMENT, cField CHAR, iField INT, nField DECIMAL (8,2));
insert into %(tableName)s (cField, iField, nField) values ("Paul Keith McNett", 23, 23.23);
insert into %(tableName)s (cField, iField, nField) values ("Edward Leafe", 42, 42.42);
insert into %(tableName)s (cField, iField, nField) values ("Carl Karsten", 10223, 23032.76);

create table %(childTableName)s (pk INTEGER PRIMARY KEY AUTOINCREMENT, parent_fk INT, cInvNum CHAR);
insert into %(childTableName)s (parent_fk, cInvNum) values (1, "IN00023");
insert into %(childTableName)s (parent_fk, cInvNum) values (1, "IN00455");
insert into %(childTableName)s (parent_fk, cInvNum) values (3, "IN00024");
""" % locals())

	def createNullRecord(self):
		self.biz._CurrentCursor.AuxCursor.execute("""
insert into %s (cField, iField, nField) values (NULL, NULL, NULL)
""" % self.temp_table_name)

	def myYield(self, eventsToProcess=wx.EVT_CATEGORY_ALL):
		"""
		Since the tests are usually run before MainLoop is called then we
		need to make our own EventLoop for Yield to actually do anything
		useful.
		"""
		evtLoop = self.app.GetTraits().CreateEventLoop()
		activator = wx.EventLoopActivator(evtLoop) # automatically restores the old one
		evtLoop.YieldFor(eventsToProcess)

	def myUpdate(self, window):
		"""
		Since Update() will not trigger paint events on Mac faster than
		1/30 of second we need to wait a little to ensure that there will
		actually be a paint event while we are yielding.
		"""
		if 'wxOSX' in wx.PlatformInfo:
			wx.MilliSleep(40)  # a little more than 1/30, just in case
		window.Update()

	def closeDialogs(self):
		"""
		Close dialogs by calling their EndModal method
		"""
		#self.myYield()
		for w in wx.GetTopLevelWindows():
			if isinstance(w, wx.Dialog):
				w.EndModal(wx.ID_CANCEL)

	def waitFor(self, milliseconds):
		intervals = milliseconds/100
		while intervals > 0:
			wx.MilliSleep(100)
			self.myYield()
			if hasattr(self, 'flag') and self.flag:
				break
			intervals -= 1

	def myExecfile(self, filename, ns):
		if not six.PY3:
			execfile(filename, ns)
		else:
			with open(filename, 'r') as f:
				source = f.read()
			exec(source, ns)

	def execSample(self, name):
		ns = Namespace()
		samplesDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../samples'))        
		self.myExecfile(os.path.join(samplesDir, name), ns.dict())
		return ns

#---------------------------------------------------------------------------

class Namespace(object):
	def dict(self):
		return self.__dict__

#---------------------------------------------------------------------------

def mybytes(text):
	if six.PY3:
		return bytes(text, 'utf-8')
	else:
		return str(text)
