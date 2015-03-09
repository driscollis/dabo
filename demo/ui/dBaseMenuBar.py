# -*- coding: utf-8 -*-
# this one will not instantiate by test.py
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dBaseMenuBar


class _dBaseMenuBar(dBaseMenuBar):
	def __init__(self):
		super(_dBaseMenuBar, self).__init__()


if __name__ == "__main__":
	from dabo.dApp import dApp
	app = dApp()
	app.setup()
	app.MainForm.MenuBar = _dBaseMenuBar()
	app.start()
