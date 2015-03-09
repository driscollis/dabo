# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dColorDialog

class _dColorDialog_test(dColorDialog):
	def show(self):
		self._selColor = None
		ret = kons.DLG_CANCEL
		res = self.ShowModal()
		if res ==  wx.ID_OK:
			ret = kons.DLG_OK
			col = self.GetColourData().GetColour()
			self._selColor = col.Red(), col.Green(), col.Blue()
		return ret

	def release(self):
		self.Destroy()

	def getColor(self):
		return self._selColor


if __name__ == "__main__":
	import test
	test.Test().runTest(_dColorDialog_test)
