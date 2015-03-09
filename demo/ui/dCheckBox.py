# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.dLocalize import _

from dabo.ui import dCheckBox


class _dCheckBox_test(dCheckBox):
	def initProperties(self):
		self.Caption = _("Do you wish to pass?")

class _dCheckBox_test3_a(dCheckBox):
	def initProperties(self):
		self.Caption = _("3-state / None; user 3-state:False")
		self.ThreeState = True
		self.Value = None

class _dCheckBox_test3_b(dCheckBox):
	def initProperties(self):
		self.Caption = _("3-state / None; user 3-state:True")
		self.ThreeState = True
		self.UserThreeState = True
		self.Value = None


if __name__ == "__main__":
	import test
	test.Test().runTest(
		(_dCheckBox_test, _dCheckBox_test3_a, _dCheckBox_test3_b))
