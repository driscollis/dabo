# -*- coding: utf-8 -*-
import re
import datetime
import wx
import dabo

from . import textboxmixin as tbm


class dTextBox(tbm.dTextBoxMixin, wx.TextCtrl):
	"""Creates a text box for editing one line of string data."""
	def __init__(self, parent, properties=None, attProperties=None, *args, **kwargs):
		self._baseClass = dTextBox
		if dabo.ui.phoenix:
			preClass = wx.TextCtrl
		else:
			preClass = wx.PreTextCtrl

		tbm.dTextBoxMixin.__init__(self, preClass, parent, properties=properties,
				attProperties=attProperties, *args, **kwargs)
