# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dPageToolBar
from dabo.ui import dPageFrame
from dabo.ui import dPageList
from dabo.ui import dPageSelect
from dabo.ui import dDockTabs
from dabo.ui import dPageStyled

from dabo.ui import dPageFrameMixin

import dabo.dEvents as dEvents
from dabo.dLocalize import _
from dabo.lib.utils import ustr

import dabo.dColors as dColors

import random

class TestMixin(object):
	def initProperties(self):
		self.Width = 600
		self.Height = 375
		self.TabPosition = random.choice(("Top", "Bottom", "Left", "Right"))

	def afterInit(self):
		self.appendPage(caption="Introduction")
		self.appendPage(caption="Chapter I")
		self.appendPage(caption="Chapter 2")
		self.appendPage(caption="Chapter 3")
		self.Pages[0].BackColor = "darkred"
		self.Pages[1].BackColor = "darkblue"
		self.Pages[2].BackColor = "green"
		self.Pages[3].BackColor = "yellow"

	def onPageChanged(self, evt):
		print("Page number changed from %s to %s" % (evt.oldPageNum, evt.newPageNum))

class _dPageToolBar_test(TestMixin, dPageToolBar):
	def afterInit(self):
		self.addImage("themes/tango/32x32/actions/go-previous.png", "Left")
		self.addImage("themes/tango/32x32/actions/go-next.png", "Right")
		self.addImage("themes/tango/32x32/actions/go-up.png", "Up")
		self.addImage("themes/tango/32x32/actions/go-down.png", "Down")
		self.appendPage(caption="Introduction", imgKey="Left")
		self.appendPage(caption="Chapter I", imgKey="Right")
		self.appendPage(caption="Chapter 2", imgKey="Up")
		self.appendPage(caption="Chapter 3", imgKey="Down")
		self.Pages[0].BackColor = "darkred"
		self.Pages[1].BackColor = "darkblue"
		self.Pages[2].BackColor = "green"
		self.Pages[3].BackColor = "yellow"

class _dPageFrame_test(TestMixin, dPageFrame): pass
class _dPageList_test(TestMixin, dPageList): pass
class _dPageSelect_test(TestMixin, dPageSelect): pass
class _dDockTabs_test(TestMixin, dDockTabs): pass
class _dPageStyled_test(TestMixin, dPageStyled):
	def initProperties(self):
		self.Width = 500
		self.Height = 250
		self.PageCount = 4
		self.TabStyle = random.choice(("Default", "VC8", "VC71", "Fancy", "Firefox"))
		self.TabPosition = random.choice(("Top", "Bottom"))
		self.ShowPageCloseButtons = random.choice((True, False))
		self.ShowDropdownTabList = random.choice((True, False))
		self.ShowMenuClose = random.choice((True, False))
		self.ShowMenuOnSingleTab = random.choice((True, False))
		self.ShowNavButtons = random.choice((True, False))
		self.MenuBackColor = "lightsteelblue"
		self.InactiveTabTextColor = "darkcyan"
		self.ActiveTabTextColor = "blue"

	def afterInit(self):
		# Make the pages visible by setting a BackColor
		self.Pages[0].BackColor = "darkred"
		self.Pages[1].BackColor = "darkblue"
		self.Pages[2].BackColor = "green"
		self.Pages[3].BackColor = "yellow"
		# Can't add controls to the Test form now, so use callAfter() to delay
		# the actual control creation.
		dabo.ui.callAfter(self._addControls)

	def _addControls(self):
		pnl = self.Form.Children[0]
		szr = pnl.Sizer
		szr.DefaultBorder = 2
		chk = dabo.ui.dCheckBox(pnl, Caption="Show Page Close Buttons",
	            DataSource=self, DataField="ShowPageCloseButtons")
		szr.append(chk, halign="center")
		chk = dabo.ui.dCheckBox(pnl, Caption="Show Nav Buttons",
	            DataSource=self, DataField="ShowNavButtons")
		szr.append(chk, halign="center")
		chk = dabo.ui.dCheckBox(pnl, Caption="Show Menu Close",
	            DataSource=self, DataField="ShowMenuClose")
		szr.append(chk, halign="center")
		lbl = dabo.ui.dLabel(pnl, Caption="Tab Style:")
		dd = dabo.ui.dDropdownList(pnl,
	            Choices=["Default", "VC8", "VC71", "Fancy", "Firefox"],
	            DataSource=self, DataField="TabStyle")
		hsz = dabo.ui.dSizer("h")
		hsz.append(lbl)
		hsz.append(dd)
		szr.append(hsz, halign="center")
		lbl = dabo.ui.dLabel(pnl, Caption="Tab Position:")
		dd = dabo.ui.dDropdownList(pnl, Choices=["Top", "Bottom"],
	            DataSource=self, DataField="TabPosition")
		hsz = dabo.ui.dSizer("h")
		hsz.append(lbl)
		hsz.append(dd)
		szr.append(hsz, halign="center")
		self.Form.layout()
		self.Form.fitToSizer()

def onPageChanged(self, evt):
	print("Page number changed from %s to %s" % (evt.oldPageNum, evt.newPageNum))



if __name__ == "__main__":
	import test
	t = test.Test()
	t.runTest(_dPageFrame_test)
	t.runTest(_dPageToolBar_test)
	t.runTest(_dPageList_test)
	t.runTest(_dPageSelect_test)
	t.runTest(_dDockTabs_test)
	t.runTest(_dPageStyled_test)
