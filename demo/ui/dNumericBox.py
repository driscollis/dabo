# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dNumericBox

from decimal import Decimal


class _dNumbericBox_test(dNumericBox):
	def initProperties(self):
		self.Value = Decimal("1.23")
		self.DecimalWidth = 3

class _dNumbericBox_test2(dNumericBox):
	def initProperties(self):
		self.Value = Decimal("23")
		self.DecimalWidth = 0

			
if __name__ == "__main__":
	import test
	test.Test().runTest((_dNumbericBox_test, _dNumbericBox_test2))
