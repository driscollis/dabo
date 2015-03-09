# -*- coding: utf-8 -*-
import wx
import dabo
from . import textboxmixin as tbm
import dabo.dEvents as dEvents
from dabo.dLocalize import _
from dabo.ui import makeDynamicProperty


# The EditBox is just a TextBox with some additional styles.
class dEditBox(tbm.dTextBoxMixin, wx.TextCtrl):
	"""
	Creates an editbox, which allows editing of string data of unlimited size.

	The editbox will create scrollbars as necessary, and can edit string or
	unicode data.
	"""
	def __init__(self, parent, properties=None, attProperties=None, *args, **kwargs):
		self._baseClass = dEditBox

		if dabo.ui.phoenix:
			preClass = wx.TextCtrl
		else:
			preClass = wx.PreTextCtrl
		kwargs["style"] = wx.TE_MULTILINE
		self._wordWrap = self._extractKey((properties, attProperties, kwargs),
				"WordWrap", True)
		if self._wordWrap:
			kwargs["style"] = kwargs["style"] | wx.TE_BESTWRAP
		else:
			kwargs["style"] = kwargs["style"] | wx.TE_DONTWRAP
		tbm.dTextBoxMixin.__init__(self, preClass, parent, properties=properties,
				attProperties=attProperties, *args, **kwargs)


	def scrollToBeginning(self):
		"""Moves the insertion point to the beginning of the text"""
		self.SetInsertionPoint(0)
		self.ShowPosition(0)
		self.Refresh()


	def scrollToEnd(self):
		"""Moves the insertion point to the end of the text"""
		self.SetInsertionPointEnd()
		self.ShowPosition(self.GetLastPosition())
		self.Refresh()


	#Property getters and setters
	def _getWordWrap(self):
		return self._wordWrap

	def _setWordWrap(self, val):
		self._wordWrap = val
		self._delWindowStyleFlag(wx.TE_DONTWRAP)
		self._delWindowStyleFlag(wx.TE_WORDWRAP)
		self._delWindowStyleFlag(wx.TE_BESTWRAP)
		if val:
			self._addWindowStyleFlag(wx.TE_BESTWRAP)
		else:
			self._addWindowStyleFlag(wx.TE_DONTWRAP)

	def _getProcessTabs(self):
		return self._hasWindowStyleFlag(wx.TE_PROCESS_TAB)

	def _setProcessTabs(self, val):
		if val:
			self._addWindowStyleFlag(wx.TE_PROCESS_TAB)
		else:
			self._delWindowStyleFlag(wx.TE_PROCESS_TAB)


	# property definitions follow:
	ProcessTabs = property(_getProcessTabs, _setProcessTabs, None,
			_("""Specifies whether the user can enter tabs in the control."""))

	WordWrap = property(_getWordWrap, _setWordWrap, None,
			_("""Specifies whether lines longer than the width of the control
			get wrapped. This is a soft wrapping; newlines are not inserted.

			If False, a horizontal scrollbar will appear when a line is
			too long to fit in the horizontal space. Note that this must
			be set when the object is created, and changing it after
			instantiation will have no effect. Default=True  (bool)"""))
