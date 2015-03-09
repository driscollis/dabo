# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dFormMain


class _dFormMain_test(dFormMain):
	pass

if __name__ == "__main__":
	import test
	test.Test().runTest(_dFormMain_test)
