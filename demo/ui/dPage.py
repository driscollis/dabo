#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dabo
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dPage

from dabo.dLocalize import _


class _dPage_test(dPage):
	def initProperties(self):
		self.BackColor = "Red"


if __name__ == "__main__":
	import test
	test.Test().runTest(_dPage_test)
