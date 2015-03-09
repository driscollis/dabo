#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dEditor


class _dEditor_test(dEditor):
	def afterInit(self):
		self.Language = "Python"

if __name__ == '__main__':
	import test
	test.Test().runTest(_dEditor_test)