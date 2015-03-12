# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dToolBar


class _dToolBar_test(dToolBar):
	def initProperties(self):
		self.MaxWidth = 22
		self.MaxHeight = 22

	def afterInit(self):
		iconPath = "themes/tango/22x22"
		self.appendButton("Copy", pic="%s/actions/edit-copy.png" % iconPath,
				toggle=False, OnHit=self.onCopy,
				tip="Copy", help="Much Longer Copy Help Text")

		self.appendButton("Toggle", pic="%s/actions/system-shutdown.png" % iconPath,
				toggle=True, OnHit=self.onToggle, tip="Toggle me", help="Toggle me")

		self.appendButton("Dabo", pic="daboIcon128", toggle=True, tip="Dabo! Dabo! Dabo!",
				help="Large icon resized to fit in the max dimensions")

		self.appendSeparator()

		self.appendButton("Exit", pic="%s/actions/system-log-out.png" % iconPath,
				toggle=True, OnHit=self.onExit,
				tip="Exit", help="Quit the application")

	def onCopy(self, evt):
		dabo.ui.info("Copy Clicked!")

	def onToggle(self, evt):
		item = evt.EventObject
		dabo.ui.info("CHECKED: %s, ID: %s" % (item.Value, item.GetId()))

	def onExit(self, evt):
		app = self.Application
		if app:
			app.onFileExit(None)
		else:
			dabo.ui.stop("Sorry, there isn't an app object - can't exit.")


if __name__ == "__main__":
	import test
	test.Test().runTest(_dToolBar_test)
