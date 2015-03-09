# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dCollapsiblePanel
from dabo.dLocalize import _


class _CollapsiblePanelTest(dCollapsiblePanel):

	def initProperties(self):
		self.Caption = "Collapsible Panel Test"

	def createItems(self):
		panel = self.Panel
		gs = dabo.ui.dGridSizer(MaxCols=2)
		gs.append(dabo.ui.dTextBox(panel), "expand")
		gs.append(dabo.ui.dButton(panel, Caption=u"Test"), "expand")
		gs.setColExpand(True, (0, 1))
		panel.Sizer = gs


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_CollapsiblePanelTest)
