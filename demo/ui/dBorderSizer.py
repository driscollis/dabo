# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dForm
from dabo.ui import dBorderSizer


class TestForm(dForm):
	def afterInit(self):
		self.Sizer = dabo.ui.dSizer("v", DefaultBorder=10)
		lbl = dabo.ui.dLabel(self, Caption="Button in BoxSizer Below", FontSize=16)
		self.Sizer.append(lbl, halign="center")
		sz = dBorderSizer(self, "v")
		self.Sizer.append1x(sz)
		btn = dabo.ui.dButton(self, Caption="Click")
		sz.append1x(btn)
		pnl = dabo.ui.dPanel(self, BackColor="seagreen")
		self.Sizer.append1x(pnl, border=18)

class _dBorderSizer_test(dBorderSizer):
	def __init__(self, bx=None, *args, **kwargs):
		super(_dBorderSizer_test, self).__init__(box=bx, orientation="h", *args, **kwargs)


if __name__ == "__main__":
	from dabo.dApp import dApp
	app = dApp()
	app.MainFormClass = TestForm
	app.start()
