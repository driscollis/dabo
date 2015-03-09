# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dHyperLink


class _dHyperLink_test(dHyperLink):
	def _onHit(self, evt):
		print("hit")


	def afterInit(self):
		self.Caption = "The Dabo Wiki"
		self.FontSize = 24
		self.URL = "http://dabodev.com/wiki/"
		self.LinkColor = "olive"
		self.VisitedColor = "maroon"
		self.HoverColor = "crimson"
		self.LinkUnderline = True
		self.HoverUnderline = False
		self.VisitedUnderline = True
		self.bindEvent(dabo.dEvents.Hit, self._onHit)
		#self.ShowInBrowser = False


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dHyperLink_test)
