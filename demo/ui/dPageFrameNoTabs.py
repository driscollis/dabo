# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dPage
from dabo.ui import dPageFrameNoTabs

import dabo.dEvents as dEvents
import dabo.dColors as dColors

import random


class TestPage(dPage):
	def afterInit(self):
		self.lbl = dabo.ui.dLabel(self, FontSize=36)
		color = random.choice(list(dColors.colorDict.keys()))
		self.BackColor = self.lbl.Caption = color
		self.Sizer = sz = dabo.ui.dSizer("h")
		sz.appendSpacer(1, 1)
		sz.append(self.lbl, 1)
		sz.appendSpacer(1, 1)

	def setLabel(self, txt):
		self.lbl.Caption = txt
		self.layout()


class _dPageFrameNoTabs_test(dabo.ui.dForm):
	def afterInit(self):
		self.Caption = "Tabless Pageframe Example"
		self.pgf = pgf = dPageFrameNoTabs(self)
		pgf.PageClass = TestPage
		pgf.PageCount = 12
		idx = 0
		for pg in pgf.Pages:
			pg.setLabel("Page #%s" % idx)
			idx += 1
		self.Sizer.append1x(pgf)

		# Add prev/next buttons
		bp = dabo.ui.dButton(self, Caption="Prior")
		bp.bindEvent(dEvents.Hit, self.onPriorPage)
		bn = dabo.ui.dButton(self, Caption="Next")
		bn.bindEvent(dEvents.Hit, self.onNextPage)
		hsz = dabo.ui.dSizer("h")
		hsz.append(bp, 1)
		hsz.appendSpacer(4)
		hsz.append(bn, 1)
		hsz.appendSpacer(24)
		lbl = dabo.ui.dLabel(self, Caption="Select Page:")
		hsz.append(lbl)
		dd = dabo.ui.dDropdownList(self, DataSource=pgf,
				DataField="SelectedPageNumber", ValueMode="Position",
				Choices=["%s" % ii for ii in range(pgf.PageCount)])
		hsz.append(dd)
		self.Sizer.append(hsz, halign="center", border=8)
		self.layout()


	def onPriorPage(self, evt):
		self.pgf.priorPage()
		self.update()

	def onNextPage(self, evt):
		self.pgf.nextPage()
		self.update()


if __name__ == '__main__':
	import test
	test.Test().runTest(_dPageFrameNoTabs_test)

