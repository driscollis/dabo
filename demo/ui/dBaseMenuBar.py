# -*- coding: utf-8 -*-
# this one will not instantiate by test.py
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dBaseMenuBar


class dBaseMenuBar(dBaseMenuBar):
	def __init__(self):
		super(_dBaseMenuBar_test, self).__init__()


if __name__ == "__main__":
	from dabo.dApp import dApp
	app = dApp()
	app.setup()
	app.MainForm.MenuBar = _dBaseMenuBar_test()
	app.start()
