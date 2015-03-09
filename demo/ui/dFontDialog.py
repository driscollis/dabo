# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dFontDialog


class _dFontDialog_test(dFontDialog):
	pass


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dFontDialog_test)
