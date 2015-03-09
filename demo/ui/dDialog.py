# -*- coding: utf-8 -*-
# this one will not instantiate by test.py
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dDialog
from dabo.ui import dStandardButtonDialog
from dabo.ui import dOkCancelDialog
from dabo.ui import dYesNoDialog


if __name__ == "__main__":
	from . import test
	test.Test().runTest(dDialog)
	test.Test().runTest(dStandardButtonDialog)
	test.Test().runTest(dOkCancelDialog)
	test.Test().runTest(dYesNoDialog)
