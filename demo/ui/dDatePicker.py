# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dDatePicker
from dabo.dLocalize import _

import datetime

class _dDatePicker_test(dDatePicker):

	def onValueChanged(self, evt):
		print("onValueChanged")


if __name__ == "__main__":
	import test

	test.Test().runTest(_dDatePicker_test, AllowNullDate=True, Value=datetime.date(1970, 12, 3))
	test.Test().runTest(_dDatePicker_test, BackColor="orange", PickerMode="Spin", AllowNullDate=True)
