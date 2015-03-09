# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dDateTextBox


class _dDateTextBox_test(dDateTextBox):
	pass


if __name__ == "__main__":
	import test
	test.Test().runTest((dDateTextBox, dDateTextBox))
