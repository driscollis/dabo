# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dSplitForm

import dabo.dColors as dColors


class _dSplitForm_test(dSplitForm):
	def initProperties(self):
		self.Caption = "Splitter Demo"

	def afterInit(self):
		self.Splitter.Panel1.BackColor = dColors.randomColor()
		self.Splitter.Panel2.BackColor = dColors.randomColor()


if __name__ == "__main__":
	import test
	test.Test().runTest(_dSplitForm_test)
