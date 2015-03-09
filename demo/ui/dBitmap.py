# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dBitmap


class _dBitmap_test(dBitmap):
	def initProperties(self):
		self.Picture = "daboIcon016"

if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dBitmap_test)
