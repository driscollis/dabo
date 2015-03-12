# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dShellForm


def main():
	from dabo.dApp import dApp
	app = dApp(BasePrefKey="dabo.ui.dShellForm")
	app.MainFormClass = dShellForm
	app.setup()
	app.start()

if __name__ == "__main__":
	main()
