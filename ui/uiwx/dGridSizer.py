import wx
import dabo
import dPemMixin
import dSizerMixin
from dabo.dLocalize import _
from dabo.ui import makeDynamicProperty
import warnings


class dGridSizer(wx.GridBagSizer, dSizerMixin.dSizerMixin):
	def __init__(self, vgap=3, hgap=3, maxRows=0, maxCols=0, **kwargs):
		"""dGridSizer is a sizer that can lay out items in a virtual grid arrangement.
		Items can be placed is specific row/column positions if that position is
		unoccupied. You can specify either MaxCols or MaxRows, and then append
		items to the grid sizer; it will place them in the first open row/col
		position, until the Max* dimension is reached; after that, it starts over in
		the next row/col. This allows for easily adding items without having to
		explicitly track each one's row/col. For example, if I have a bunch of 
		labels and edit controls to add, and I want them in a grid arrangement
		with labels on the left and controls on the right, I can set MaxCols to 2, 
		and then append label, control, label, control, ..., and the dGridSizer
		will automatically arrange them as desired.
		"""
		self._baseClass = dGridSizer
		self._parent = None
		# Save these values, as there is no easy way to determine them
		# later
		self.hgap = hgap
		self.vgap = vgap
		
		wx.GridBagSizer.__init__(self, vgap=vgap, hgap=hgap)
		
		self._maxRows = 0
		self._maxCols = 0
		self._maxDimension = "c"
		if not maxRows and not maxCols:
			# No max settings were passed, so default to 2 columns
			self.MaxCols = 2
		elif maxCols:
			self.MaxCols = maxCols
		else:
			# Rows were passed.
			self.MaxRows = maxRows
		self.SetFlexibleDirection(self.bothFlag)
		# Keep track of the highest numbered row/col that
		# contains an item
		self._highRow = self._highCol = -1

		for k,v in kwargs.items():
			try:
				exec("self.%s = %s" % (k,v))
			except: pass


	def append(self, item, layout="normal", row=-1, col=-1, 
			rowSpan=1, colSpan=1, alignment=None, halign="left", 
			valign="middle", border=0, borderSides=("all",), 
			borderFlags=("all",), flag=None):
		""" Inserts the passed item at the specified position in the grid. If no
		position is specified, the item is inserted at the first available open 
		cell as specified by the Max* properties.		
		"""
		if borderSides is None:
			if borderFlags is not None:
				dabo.errorLog.write(_("Depracation warning: use 'borderSides' parameter instead."))
				borderSides = borderFlags
		(targetRow, targetCol) = self._determineAvailableCell(row, col)
		if isinstance(item, (tuple, int)):
			# spacer
			if isinstance(item, int):
				item = (item, item)
			szItem = self.Add(item, (targetRow, targetCol), span=(rowSpan, colSpan) )
			spc = szItem.GetSpacer()
			spc._controllingSizer = self
			spc._controllingSizerItem = szItem
			szItem.ControllingSizer = self
		else:
			# item is the window to add to the sizer
			_wxFlags = self._getWxFlags(alignment, halign, valign, borderSides, layout)
			if flag:
				_wxFlags = _wxFlags | flag
			szItem = self.Add(item, (targetRow, targetCol), span=(rowSpan, colSpan), 
					flag=_wxFlags, border=border)
			item._controllingSizer = self
			item._controllingSizerItem = szItem
			szItem.ControllingSizer = self
			
		self._highRow = max(self._highRow, targetRow)
		self._highCol = max(self._highCol, targetCol)
		return szItem
		
		
	def appendItems(self, items, *args, **kwargs):
		""" Shortcut for appending multiple items at once. """
		ret = []
		for item in items:
			ret.append(self.append(item, *args, **kwargs))
		return ret
	
	
	def appendSpacer(self, *args, **kwargs):
		"""Alias for append()"""
		return self.append(*args, **kwargs)
		
		
	def insert(self, *args, **kwargs):
		""" This is not supported for this type of sizer """
		raise NotImplementedError, _("Grid Sizers do not support insert()")
	
	
	def removeRow(self, rowNum):
		""" Deletes any items contained in the specified row, and
		then moves all items below it up to fill the space.
		"""
		for c in range(self._highCol+1):
			szitm = self.FindItemAtPosition( (rowNum, c) )
			if not szitm:
				continue
			itm = None
			if szitm.IsWindow():
				itm = szitm.GetWindow()
				self.remove(itm)
				itm.Destroy()
			elif szitm.IsSizer():
				szr = szitm.GetSizer()
				# Release the sizer and its contents
				self.remove(szr)
				szr.release(True)
			elif szitm.IsSpacer():
				itm = szitm.GetSpacer()
				self.remove(itm)
		# OK, all items are removed. Now move all higher rows upward
		for r in range(rowNum+1, self._highRow+1):
			for c in range(self._highCol+1):
				self.moveCell(r, c, r-1, c, delay=True)
		self.layout()
		self._highRow -= 1
		
		
	def removeCol(self, colNum):
		""" Deletes any items contained in the specified column, and
		then moves all items to the right of it up to fill the space.
		"""
		for r in range(self._highRow+1):
			szitm = self.FindItemAtPosition( (r, colNum) )
			if not szitm:
				continue
			itm = None
			if szitm.IsWindow():
				itm = szitm.GetWindow()
				self.remove(itm)
				itm.Destroy()
			elif szitm.IsSizer():
				szr = szitm.GetSizer()
				self.remove(szr)
				# Release the sizer and its contents
				szr.release(True)
			elif szitm.IsSpacer():
				itm = szitm.GetSpacer()
				self.remove(itm)
		# OK, all items are removed. Now move all higher columns to the left
		for r in range(self._highRow+1):
			for c in range(colNum+1, self._highCol+1):
				self.moveCell(r, c, r, c-1, delay=True)
		self.layout()
		self._highCol -= 1
		
		
	def setColExpand(self, expand, colNum, proportion=0):
		""" Sets the 'growable' status of one or more columns. """
		# If the colNum argument was passed first, switch it with the 
		# expand argument
		if isinstance(expand, basestring):
			expand, colNum = colNum, expand
		if isinstance(colNum, (list, tuple)):
			for col in colNum:
				self.setColExpand(expand, col, proportion)
		elif isinstance(colNum, basestring):
			if colNum.lower() == "all":
				chldrn = self.GetChildren()
				c = {}
				for chld in chldrn:
					(row, col) = chld.GetPosTuple()
					c[col] = True
				for column in c.keys():
					self.setColExpand(expand, column, proportion)
		else:
			curr = self.getColExpand(colNum)
			if expand and not curr:
				self.AddGrowableCol(colNum, proportion=proportion)
			elif not expand and curr:
				self.RemoveGrowableCol(colNum)
		self.layout()
		
		
	def setRowExpand(self, expand, rowNum, proportion=0):
		""" Sets the 'growable' status of one or more rows. """
		# If the rowNum argument was passed first, switch it with the 
		# expand argument
		if isinstance(expand, basestring):
			expand, rowNum = rowNum, expand
		if isinstance(rowNum, (list, tuple)):
			for row in rowNum:
				self.setRowExpand(expand, row, proportion)
		elif isinstance(rowNum, basestring):
			if rowNum.lower() == "all":
				chldrn = self.GetChildren()
				r = {}
				for chld in chldrn:
					(row, col) = chld.GetPosTuple()
					r[row] = True
				for row in r.keys():
					self.setRowExpand(expand, row, proportion)
		else:
			curr = self.getRowExpand(rowNum)
			if expand and not curr:
				self.AddGrowableRow(rowNum, proportion=proportion)
			elif not expand and curr:
				self.RemoveGrowableRow(rowNum)
		self.layout()
		
		
	def setFullExpand(self):
		"""Convenience method for setting all columns and rows of the 
		sizer to be growable. Must be called after all items are added,
		as any rows or columns added after the call will be the default
		of non-growable.
		"""
		self.setColExpand(True, "all")
		self.setRowExpand(True, "all")
		
	
	def setFullCollapse(self):
		"""Convenience method for setting all columns and rows of the 
		sizer to not be growable.
		"""
		self.setColExpand(False, "all")
		self.setRowExpand(False, "all")
		
	
	def isRowGrowable(self, row):
		warnings.warn("Deprecated; use 'getRowExpand' instead.", DeprecationWarning)
		return self.getRowExpand(row)
	
	
	def getRowExpand(self, row):
		"""Returns True if the specified row is growable."""
		# If the row isn't growable, it will throw an error
		ret = True
		try:
			self.RemoveGrowableRow(row)
			self.AddGrowableRow(row)
		except:
			ret = False
		return ret
		
		
	def isColGrowable(self, col):
		warnings.warn("Deprecated; use 'getColExpand' instead.", DeprecationWarning)
		return self.getColExpand(col)


	def getColExpand(self, col):
		"""Returns True if the specified column is growable."""
		# If the col isn't growable, it will throw an error
		ret = True
		try:
			self.RemoveGrowableCol(col)
			self.AddGrowableCol(col)
		except:
			ret = False
		return ret
		
		
	def moveCell(self, fromRow, fromCol, toRow, toCol, delay=False):
		""" Move the contents of the specified cell to the target
		location. By default, layout() is called; this can be changed when 
		moving a number of cells by specifying delay=True. In this
		event, the calling code is responsible for calling layout() when all
		the moving is done.
		"""
		sz = self.FindItemAtPosition( (fromRow, fromCol) )
		if sz:
			if sz.IsWindow():
				obj = sz.GetWindow()
				self.moveObject(obj, toRow, toCol, delay=delay)

			
	def moveObject(self, obj, targetRow, targetCol, delay=False):
		"""Moves the object to the given row/col if possible."""
		self.SetItemPosition(obj, (targetRow, targetCol) )
		if not delay:
			self.layout()
		
		
	def _determineAvailableCell(self, row, col):
		(targetRow, targetCol) = (row, col)
		if (row == -1) or (col == -1):
			# Get the first available cell
			(emptyRow, emptyCol) = self.findFirstEmptyCell()
			if row == -1:
				targetRow = emptyRow
			if col == -1:
				targetCol = emptyCol
		return (targetRow, targetCol)
		
				
	def findFirstEmptyCell(self):
		""" The idea is this: use the MaxDimension to determine how
		we look through the grid. When we find an empty cell, return
		its coordinates.
		"""
		ret = ()
		if self.MaxDimension == "c":
			emptyRow = 0
			maxCol = max(1, self.MaxCols)
			while not ret:
				for c in range(maxCol):
					if not self.FindItemAtPosition( (emptyRow, c) ):
						# Empty!
						ret = (emptyRow, c)
						break
				emptyRow += 1
		else:
			emptyCol = 0
			maxRow = max(1, self.MaxRows)
			while not ret:
				for r in range(maxRow):
					if not self.FindItemAtPosition( (r, emptyCol) ):
						# Empty!
						ret = (r, emptyCol)
						break
				emptyCol += 1
		return ret
	
	
	def getHighRow(self):
		"""Returns the highest row that contains an object."""
		rows = [self.GetItemPosition(win)[0] + (self.GetItemSpan(win)[0]-1)
				for win in self.ChildWindows]
		return max(rows)
	
	
	def getHighCol(self):
		"""Returns the highest column that contains an object."""
		cols = [self.GetItemPosition(win)[1] + (self.GetItemSpan(win)[1]-1)
				for win in self.ChildWindows]
		return max(cols)
	
	
	def getGridPos(self, obj):
		"""Given an object that is contained in this grid
		sizer, returns a (row,col) tuple for that item's location.
		"""
		if isinstance(obj, self.GridSizerItem):
			obj = self.getItem(obj)
		try:
			row, col = self.GetItemPosition(obj)
		except:
			# Window isn't controlled by this sizer
			row, col = None, None
		return (row, col)


	def getGridSpan(self, obj):
		"""Given an object that is contained in this grid
		sizer, returns a (row,col) tuple for that item's cell span.
		"""
		if isinstance(obj, self.GridSizerItem):
			obj = self.getItem(obj)
		try:
			row, col = self.GetItemSpan(obj)
		except wx.PyAssertionError, e:
			# Window isn't controlled by this sizer
			row, col = None, None
		return (row, col)
	
	
	def setGridSpan(self, obj, row=None, col=None):
		"""Given an object that is contained in this grid
		sizer, sets its span to the given values. Returns 
		True if successful, or False if it fails, due to another
		item in the way.
		"""
		if isinstance(obj, self.GridSizerItem):
			obj = self.getItem(obj)
		currRow, currCol = self.getGridSpan(obj)
		if row is None:
			row = currRow
		if col is None:
			col = currCol
		spn = wx.GBSpan(row, col)
		try:
			self.SetItemSpan(obj, spn)
		except:
			raise dabo.ui.GridSizerSpanException, _("An item already exists in that location")
	
	
	def setRowSpan(self, obj, rowspan):
		"""Sets the row span, keeping the col span the same."""
		self.setGridSpan(obj, row=rowspan)
		
	
	def setColSpan(self, obj, colspan):
		"""Sets the col span, keeping the row span the same."""
		self.setGridSpan(obj, col=colspan)
		
	
	def getItemByRowCol(self, row, col, returnObject=True):
		"""Returns either the managed item or the sizer item at the 
		given position if one exists. If not, returns None.
		"""
		try:
			itm = self.FindItemAtPosition((row, col))
			if returnObject:
				if itm.IsWindow():
					ret = itm.GetWindow()
				elif itm.IsSizer():
					ret = itm.GetSizer()
			else:
				# Return the sizer item itself.
				ret = itm
		except:
			ret = None
		return ret
	
	
	def getNeighbor(self, obj, dir):
		"""Returns the object adjacent to the given object. Possible
		values for 'dir' are: left, right, up, down.
		"""
		dir = dir[0].lower()
		if dir not in "lrud":
			return None		
		offsets = {"l" : (0, -1), "r" : (0, 1), "u" : (-1, 0), "d" : (1, 0)}
		off = offsets[dir]
		return self.getItemAtOffset(obj, off)
		
	
	def getItemAtOffset(self, obj, off):
		"""Given an object and a (row, col) offset, returns
		the object at the offset position, or None if no such 
		object exists.
		"""
		row, col = self.getGridPos(obj)
		newRow = row + off[0]
		newCol = col + off[1]
		try:
			ret = self.getItemByRowCol(newRow, newCol)
		except:
			ret = None
		return ret

	
	def getItemProp(self, itm, prop):
		if not isinstance(itm, (self.SizerItem, self.GridSizerItem)):
			itm = itm.ControllingSizerItem
		ret = None
		if itm.IsWindow():
			chil = itm.GetWindow()
		else:
			chil = itm.GetSizer()
		row, col = self.getGridPos(chil)
		lowprop = prop.lower()
		if lowprop == "border":
			return itm.GetBorder()
		elif lowprop == "rowexpand":
			ret = self.getRowExpand(row)
		elif lowprop == "colexpand":
			ret = self.getColExpand(col)
		elif lowprop == "rowspan":
			ret = self.GetItemSpan(chil).GetRowspan()
		elif lowprop == "colspan":
			ret = self.GetItemSpan(chil).GetColspan()
		elif lowprop == "proportion":
			ret = itm.GetProportion()
		else:
			# Property is in the flag setting.
			flag = itm.GetFlag()
			szClass = dabo.ui.dSizer
			if lowprop == "halign":
				if flag & szClass.rightFlag:
					ret = "Right"
				elif flag & szClass.centerFlag:
					ret = "Center"
				else: 		#if flag & szClass.leftFlag:
					ret = "Left"
			elif lowprop == "valign":
				if flag & szClass.middleFlag:
					ret = "Middle"
				elif flag & szClass.bottomFlag:
					ret = "Bottom"
				else:		#if flag & szClass.topFlag:
					ret = "Top"
			elif lowprop == "expand":
				return bool(flag & szClass.expandFlag)
			elif lowprop == "bordersides":
				pdBorder = {"Bottom" : self.borderBottomFlag,
						"Left" : self.borderLeftFlag,
						"Right" : self.borderRightFlag, 
						"Top" : self.borderTopFlag}
				if flag & self.borderAllFlag:
					ret = ["All"]
				else:
					ret = []
					for side, val in pdBorder.items():
						if flag and val:
							ret.append(key)
					if not ret:
						ret = ["None"]
		if ret is None:
			print "NO PROP:", prop, itm
		return ret
		
					
	def copyGrid(self, oldGrid):
		""" This method takes an existing GridSizer, and moves
		the contents to the current grid. The properties of each
		cell's item are preserved, but row/column Expand settings 
		must be handled separately.
		"""
		for r in range(oldGrid._highRow+1):
			for c in range(oldGrid._highCol+1):
				szitm = oldGrid.FindItemAtPosition( (r,c) )
				itm = oldGrid.getItem(szitm)
				if itm is None:
					continue
				f = szitm.GetFlag()
				oldGrid.remove(itm)
				self.append(itm, flag=f)


	def drawOutline(self, win, recurse=False):
		""" Need to override this method to draw the outline
		properly for the grid.
		"""
		dc = wx.ClientDC(win)
		dc.SetBrush(wx.TRANSPARENT_BRUSH)
		dc.SetLogicalFunction(wx.COPY)
		x, y = self.GetPosition()
		w, h = self.GetSize()
		rows = self.GetRows()
		cols = self.GetCols()
		vgap = self.GetVGap()
		hgap = self.GetHGap()
		x2,y2 = x,y
		rhts = self.GetRowHeights()
		dc.SetPen(wx.Pen("blue", 1, wx.SOLID))
		for hh in rhts:
			dc.DrawRectangle(x2, y2, w, hh)
			y2 += hh+vgap
		x2 = x
		y2 = y
		cwds = self.GetColWidths()
		dc.SetPen(wx.Pen("red", 1, wx.SOLID))
		for ww in cwds:
			dc.DrawRectangle(x2, y2, ww, h)
			x2 += ww+hgap
		dc.SetPen(wx.Pen("green", 3, wx.LONG_DASH))
		dc.DrawRectangle(x,y,w,h)
		
		for ch in self.Children:
			if ch.IsSizer():
				sz = ch.GetSizer()
				if hasattr(sz, "drawOutline"):
					sz.drawOutline(win, recurse)
			elif ch.IsWindow():
				w = ch.GetWindow()
				if isinstance(w, dabo.ui.dPageFrame):
					w = w.SelectedPage
				if hasattr(w, "Sizer") and w.Sizer:	
					w.Sizer.drawOutline(w, True)
	
	
	def _getHGap(self):
		return self.GetHGap()
	
	def _setHGap(self, val):
		if isinstance(val, basestring):
			val = int(val)
		self.SetHGap(val)
		
		
	def _getMaxRows(self):
		return self._maxRows
	
	def _setMaxRows(self, rows):
		if isinstance(rows, basestring):
			rows = int(rows)
		self._maxRows = rows
		if rows:
			self.MaxDimension = "r"
			self.MaxCols = 0
		
		
	def _getMaxCols(self):
		return self._maxCols
	
	def _setMaxCols(self, cols):
		if isinstance(cols, basestring):
			cols = int(cols)
		self._maxCols = cols
		if cols:
			self.MaxDimension = "c"
			self.MaxRows = 0
	
	
	def _getMaxDimension(self):
		return self._maxDimension
	
	def _setMaxDimension(self, val):
		self._maxDimension = val
		
	
	def _getVGap(self):
		return self.GetVGap()
	
	def _setVGap(self, val):
		if isinstance(val, basestring):
			val = int(val)
		self.SetVGap(val)
		
	
	HGap = property(_getHGap, _setHGap, None,
			_("Horizontal gap between cells in the sizer  (int)"))
			
	MaxRows = property(_getMaxRows, _setMaxRows, None,
			_("When adding elements to the sizer, controls the max number "
			"of rows to add before a new column is started. (int)") )

	MaxCols = property(_getMaxCols, _setMaxCols, None,
			_("When adding elements to the sizer, controls the max number "
			"of columns to add before a new row is started. (int)") )

	MaxDimension = property(_getMaxDimension, _setMaxDimension, None,
			_("When adding elements to the sizer, this property determines "
			" if we use rows or columns as the limiting value. (char: 'r' or 'c'(default) )") )
	
	Orientation = property(_getMaxDimension, _setMaxDimension, None, 
			_("Alias for the MaxDimensions property. (char: 'r' or 'c'(default) )") )
			
	VGap = property(_getVGap, _setVGap, None,
			_("Vertical gap between cells in the sizer  (int)"))
	
	
	DynamicHGap = makeDynamicProperty(HGap)
	DynamicMaxRows = makeDynamicProperty(MaxRows)
	DynamicMaxCols = makeDynamicProperty(MaxCols)
	DynamicMaxDimension = makeDynamicProperty(MaxDimension)
	DynamicOrientation = makeDynamicProperty(Orientation)
	DynamicVGap = makeDynamicProperty(VGap)


if __name__ == "__main__":
	s = dGridSizer()
