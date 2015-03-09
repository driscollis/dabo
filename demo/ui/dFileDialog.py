# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dFileDialog
from dabo.ui import dFolderDialog
from dabo.ui import dSaveDialog


class _dFileDialog_test(dFileDialog):
	pass


class _dFolderDialog_test(dFolderDialog):
	pass


class _dSaveDialog_test(dSaveDialog):
	pass


if __name__ == "__main__":
	import test
	test.Test().runTest(_dFileDialog_test)
	test.Test().runTest(_dFolderDialog_test)
	test.Test().runTest(_dSaveDialog_test)
