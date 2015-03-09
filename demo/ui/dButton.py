# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dButton


class _dButton_test(dButton):
	def initProperties(self):
		self.Caption = "You better not push me"
		self.FontSize = 8
		self.Width = 223

	def onContextMenu(self, evt):
		print("context menu")

	def onMouseRightClick(self, evt):
		print("right click")

	def onHit(self, evt):
		self.ForeColor = "purple"
		self.FontBold = True
		self.FontItalic = True
		self.Caption = "Ok, you cross this line, and you die."
		self.Width = 333


if __name__ == "__main__":
	import test
	test.Test().runTest(_dButton_test)
