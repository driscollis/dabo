# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dBorderlessButton


class _dBorderlessButton_test(dBorderlessButton):
	def initProperties(self):
		self.Caption = "You better not push me"
		self.FontSize = 8
		self.Width = 223
		self.Picture = "themes/tango/32x32/apps/accessories-text-editor.png"


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
		self.Form.layout()

if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dBorderlessButton_test)
