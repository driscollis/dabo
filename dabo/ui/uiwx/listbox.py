# -*- coding: utf-8 -*-
import wx
import dabo
from . import controlitemmixin as dcm
import dabo.dEvents as dEvents
from dabo.dLocalize import _
from dabo.ui import makeDynamicProperty


class dListBox(dcm.dControlItemMixin, wx.ListBox):
	"""Creates a listbox, allowing the user to choose one or more items."""
	def __init__(self, parent, properties=None, attProperties=None, *args, **kwargs):
		self._baseClass = dListBox
		self._choices = []

		if dabo.ui.phoenix:
			preClass = wx.ListBox
		else:
			preClass = wx.PreListBox
		dcm.dControlItemMixin.__init__(self, preClass, parent, properties=properties,
				attProperties=attProperties, *args, **kwargs)


	def _initEvents(self):
		super(dListBox, self)._initEvents()
		self.Bind(wx.EVT_LISTBOX, self._onWxHit)


	def clearSelections(self):
		for elem in self.GetSelections():
			self.SetSelection(elem, False)


	def selectAll(self):
		if self.MultipleSelect:
			for ii in range(self.Count):
				self.SetSelection(ii)


	def unselectAll(self):
		self.clearSelections()


	def invertSelections(self):
		"""Switch all the items from False to True, and vice-versa."""
		for ii in range(self.Count):
			if self.IsSelected(ii):
				self.Deselect(ii)
			else:
				self.SetSelection(ii)


	def _getMultipleSelect(self):
		return self._hasWindowStyleFlag(wx.LB_EXTENDED)
	def _setMultipleSelect(self, val):
		if bool(val):
			self._delWindowStyleFlag(wx.LB_SINGLE)
			self._addWindowStyleFlag(wx.LB_EXTENDED)
		else:
			self._delWindowStyleFlag(wx.LB_EXTENDED)
			self._addWindowStyleFlag(wx.LB_SINGLE)

	MultipleSelect = property(_getMultipleSelect, _setMultipleSelect, None,
			_("Can multiple items be selected at once?  (bool)") )


	DynamicMultipleSelect = makeDynamicProperty(MultipleSelect)
