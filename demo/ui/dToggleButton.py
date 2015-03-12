# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dToggleButton

from dabo.dLocalize import _


class _dToggleButton_test(dToggleButton):
	def afterInit(self):
		self.Caption = "Toggle me!"
		self.Size = (100, 31)
		self.Picture = "themes/tango/22x22/apps/accessories-text-editor.png"
		self.DownPicture = "themes/tango/22x22/apps/help-browser.png"

	def onHit(self, evt):
		if self.Value:
			state = "down"
		else:
			state = "up"
		bval = self.Value
		self.Caption = _("State: %(state)s (Boolean: %(bval)s)") % locals()


if __name__ == "__main__":
	import test
	test.Test().runTest(_dToggleButton_test)
