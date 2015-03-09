# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dLine


class _dLine_test(dLine):
	def initProperties(self):
		self.Orientation = "Horizontal"
		self.Width = 200
		self.Height = 10


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dLine_test)
