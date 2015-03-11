# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dPanel
from dabo.ui import dScrollPanel

from dabo import dEvents


class _dPanel_test(dPanel):
	def initProperties(self):
		self.BackColor = "wheat"
		self.Hover = True

	def afterInit(self):
		self.addObject(dPanel, BackColor = "green")

	def onHover(self, evt):
		self._normBack = self.BackColor
		self.BackColor = dColors.randomColor()

	def endHover(self, evt):
		self.BackColor = self._normBack

	def onMouseLeftDown(self, evt):
		print("mousedown")

	def onPaint(self, evt):
		print("paint")

	def onKeyDown(self, evt):
		print(evt.EventData["keyCode"])


class _dScrollPanel_test(dScrollPanel):
	def initProperties(self):
		self.BackColor = "wheat"

	def afterInit(self):
		subpan = self.addObject(dPanel, BackColor = "green")
		subpan.bindEvent(dEvents.KeyDown, self.onKeyDown)
		self.SetScrollbars(10, 10, 100, 100)

	def onMouseLeftDown(self, evt):
		print("mousedown")
		self.SetFocusIgnoringChildren()

	def onPaint(self, evt):
		print("paint")

	def onKeyDown(self, evt):
		print(evt.EventData["keyCode"])

	def onScrollLineUp(self, evt):
		if evt.orientation == "Horizontal":
			print("Scroll Line Left")
		else:
			print("Scroll Line Up")

	def onScrollLineDown(self, evt):
		if evt.orientation == "Horizontal":
			print("Scroll Line Right")
		else:
			print("Scroll Line Down")

	def onScrollPageUp(self, evt):
		if evt.orientation == "Horizontal":
			print("Scroll Page Left")
		else:
			print("Scroll Page Up")

	def onScrollPageDown(self, evt):
		if evt.orientation == "Horizontal":
			print("Scroll Page Right")
		else:
			print("Scroll Page Down")



class SquarePanel(dPanel):
	def afterInit(self):
		self.Square = True
		self.BackColor = "green"

class RegularPanel(dPanel):
	def afterInit(self):
		self.Square = False
		self.BackColor = "blue"

class _SquareForm_test(dabo.ui.dForm):
	def afterInit(self):
		self.pnl = SquarePanel(self, Width=100)
		sz = self.Sizer
		sz.appendSpacer(20)
		sz.append(self.pnl,  1, "x", halign="right", valign="bottom", border=5)
		sz.appendSpacer(20)
		self.regPanel = RegularPanel(self, Width=100)
		sz.append1x(self.regPanel, halign="center", border=5)
		sz.appendSpacer(20)
		self.layout()


if __name__ == "__main__":
	import test
	test.Test().runTest(_dPanel_test)
	test.Test().runTest(_dScrollPanel_test)
	test.Test().runTest(_SquareForm_test)

