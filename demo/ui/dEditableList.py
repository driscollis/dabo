# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dEditableList
from dabo.dLocalize import _


class _dEditableList_test(dEditableList):
	def afterInit(self):
		self.Choices = ["Johnny", "Joey", "DeeDee"]
		self.Caption = "Gabba Gabba Hey"

	def onDestroy(self, evt):
		# Need to check this, because apparently under the hood
		# wxPython destroys and re-creates the control when you
		# edit, add or delete an entry.
		if self._finito:
			print("Result:", self.Choices)


if __name__ == "__main__":
	import test
	test.Test().runTest(_dEditableList_test)
