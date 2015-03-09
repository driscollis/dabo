# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dFontDialog


class _dFontDialog_test(dFontDialog):
	pass


if __name__ == "__main__":
	import test
	test.Test().runTest(_dFontDialog_test)
