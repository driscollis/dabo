# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dBitmapButton


class _dBitmapButton_test(dBitmapButton):
	def afterInit(self):
		# Demonstrate that the Picture props are working.
		self.Picture = "themes/tango/16x16/apps/accessories-text-editor.png"
		self.DownPicture = "themes/tango/16x16/apps/help-browser.png"
		self.FocusPicture = "themes/tango/16x16/apps/utilities-terminal.png"
		self.Width = 100
		self.Height = 25

if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dBitmapButton_test)
