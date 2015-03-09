# -*- coding: utf-8 -*-
import wx
import dabo
from . import controlitemmixin as dcm
from dabo.dLocalize import _


class dDropdownList(dcm.dControlItemMixin, wx.Choice):
	"""
	Creates a dropdown list, which allows the user to select one item.

	This is a very simple control, suitable for choosing from one of a handful
	of items. Only one column can be displayed. A more powerful, flexible
	control for all kinds of lists is dListControl, but dDropdownList does
	suffice for simple needs.
	"""
	def __init__(self, parent, properties=None, attProperties=None, *args, **kwargs):
		self._baseClass = dDropdownList
		self._choices = []
		if dabo.ui.phoenix:
			preClass = wx.Choice
		else:
			preClass = wx.PreChoice
		dcm.dControlItemMixin.__init__(self, preClass, parent, properties=properties,
				attProperties=attProperties, *args, **kwargs)


	def _initEvents(self):
		super(dDropdownList, self)._initEvents()
		self.Bind(wx.EVT_CHOICE, self._onWxHit)
