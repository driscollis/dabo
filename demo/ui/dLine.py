# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dLine


class _dLine_test(dLine):
	def initProperties(self):
		self.Orientation = "Horizontal"
		self.Width = 200
		self.Height = 10


if __name__ == "__main__":
	import test
	test.Test().runTest(_dLine_test)
