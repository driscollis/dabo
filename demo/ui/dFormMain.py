# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dFormMain


class _dFormMain_test(dFormMain):
	pass

if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dFormMain_test)
