# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dDateTextBox


class _dDateTextBox_test(dDateTextBox):
	pass


if __name__ == "__main__":
	from . import test
	test.Test().runTest((dDateTextBox, dDateTextBox))
