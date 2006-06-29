import wx
import  wx.lib.buttons as wxb
import warnings
import dabo

if __name__ == "__main__":
	dabo.ui.loadUI("wx")

import dDataControlMixin as dcm
import dImageMixin as dim
from dabo.dLocalize import _
import dabo.dEvents as dEvents

class dToggleButton(wxb.GenBitmapTextToggleButton, dcm.dDataControlMixin,
		dim.dImageMixin):
	"""Creates a button that toggles on and off, for editing boolean values.

	This is functionally equivilent to a dCheckbox, but visually much different.
	Also, it implies that pushing it will cause some sort of immediate action to
	take place, like you get with a normal button.
	"""
	def __init__(self, parent, properties=None, *args, **kwargs):
		self._baseClass = dabo.ui.dToggleButton
		preClass = wxb.GenBitmapTextToggleButton
		# These are required arguments
		kwargs["bitmap"] = None
		kwargs["label"] = ""
		self._downPicture = None
		dim.dImageMixin.__init__(self)
		dcm.dDataControlMixin.__init__(self, preClass, parent, properties, *args, **kwargs)
		
		self.Bind(wx.EVT_BUTTON, self.__onButton)
	
	
	def __onButton(self, evt):
		self.raiseEvent(dEvents.Hit, evt)

	
	def getBlankValue(self):
		return False


	def _getDownPicture(self):
		return self._downPicture

	def _setDownPicture(self, val):
		if self._constructed():
			self._downPicture = val
			if isinstance(val, wx.Bitmap):
				bmp = val
			else:
				bmp = dabo.ui.strToBmp(val, self._imgScale, self._imgWd, self._imgHt)
			all = not self._downPicture
			self.SetBitmapSelected(bmp)
			self.refresh()
		else:
			self._properties["DownPicture"] = val


	def _getPicture(self):
		return self._picture

	def _setPicture(self, val):
		if self._constructed():
			self._picture = val
			if isinstance(val, wx.Bitmap):
				bmp = val
			else:
				bmp = dabo.ui.strToBmp(val, self._imgScale, self._imgWd, self._imgHt)
			all = not self._downPicture
			self.SetBitmapLabel(bmp, all)
			self.refresh()
		else:
			self._properties["Picture"] = val


	DownPicture = property(_getDownPicture, _setDownPicture, None,
			_("Picture displayed when the button is pressed  (str)"))
	
	Picture = property(_getPicture, _setPicture, None,
			_("Picture used for the normal (unselected) state  (str)"))
	
		
class _dToggleButton_test(dToggleButton):
	def afterInit(self):
		self.Caption = "Toggle me!"
		self.Size = (100, 31)
		self.Picture = "uparrow"
		self.DownPicture = "downarrow"

	def onHit(self, evt):
		if self.Value:
			state = ("down", "True")
		else:
			state = ("up", "False")
		self.Caption = _("State: %s (Boolean: %s)" % state)


if __name__ == "__main__":
	import test
	test.Test().runTest(_dToggleButton_test)
