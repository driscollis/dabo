# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dForm
from dabo.ui import dSlidePanel
from dabo.ui import dSlidePanelControl

from dabo import dEvents
from dabo import dColors


class _dSlidePanelControl_test(dabo.ui.dForm):
	def afterInit(self):
		dSlidePanelControl(self, RegID="slideControl", ExpandContent=False,
	            SingleClick=True)
		self.Sizer.append1x(self.slideControl)
		self.p1 = dabo.ui.dSlidePanel(self.slideControl, Caption="First",
	            BackColor="orange")
		self.p2 = dabo.ui.dSlidePanel(self.slideControl, Caption="Second",
	            BarStyle="HorizontalFill", BarColor1="lightgreen", BarColor2="ForestGreen",
	            BackColor="wheat")
		self.p3 = dabo.ui.dSlidePanel(self.slideControl, Caption="Third",
	            BarStyle="BorderOnly", BackColor="powderblue", Border=33)

		self.p1.Sizer = dabo.ui.dSizer("v")
		btn = dabo.ui.dButton(self.p1, Caption="Change Bar 1 Style")
		self.p1.Sizer.append(btn, border=25)
		btn.bindEvent(dEvents.Hit, self.onBtn)

		self.p2.Sizer = dabo.ui.dSizer("v")
		lbl = dabo.ui.dLabel(self.p2, Caption="Tea For Two", FontItalic=True,
	            FontSize=24)
		self.p2.Sizer.append(lbl)
		def collapse3(evt):
			mc = self.slideControl
			if mc.Singleton:
				mc.expand(self.p2)
			else:
				mc.collapse(self.p3)
		self.p3.Sizer = dabo.ui.dGridSizer(HGap=5, VGap=2, MaxCols=2, DefaultBorder=3)
		lbl = dabo.ui.dLabel(self.p3, Caption="Three Strikes")
		btn = dabo.ui.dButton(self.p3, Caption="Collapse Me", OnHit=collapse3)
		self.p3.Sizer.appendItems((lbl, btn))
		# Demonstrate the grid
		self.p3.Sizer.append(dabo.ui.dLabel(self.p3, Caption="Just"))
		self.p3.Sizer.append(dabo.ui.dLabel(self.p3, Caption="taking"))
		self.p3.Sizer.append(dabo.ui.dLabel(self.p3, Caption="up"))
		self.p3.Sizer.append(dabo.ui.dLabel(self.p3, Caption="space"))
		self.p3.Sizer.append(dabo.ui.dLabel(self.p3, Caption="in"))
		self.p3.Sizer.append(dabo.ui.dLabel(self.p3, Caption="the"))
		self.p3.Sizer.append(dabo.ui.dLabel(self.p3, Caption="Grid"))
		self.p3.Sizer.append(dabo.ui.dLabel(self.p3, Caption="Sizer"))

		hsz = dabo.ui.dSizer("h")
		btnCollapse = dabo.ui.dButton(self, Caption="Collapse All")
		btnCollapse.bindEvent(dEvents.Hit, self.onCollapseAll)
		btnExpand = dabo.ui.dButton(self, Caption="Expand All")
		btnExpand.bindEvent(dEvents.Hit, self.onExpandAll)
		hsz.append(btnCollapse)
		hsz.appendSpacer(10)
		hsz.append(btnExpand)
		hsz.appendSpacer(10)
		chkSingleton = dabo.ui.dCheckBox(self, Caption="Singleton Style",
	            DataSource="self.Form.slideControl", DataField="Singleton")
		chkSingle = dabo.ui.dCheckBox(self, Caption="Single Click to Toggle",
	            DataSource="self.Form.slideControl", DataField="SingleClick")
		chkBottom = dabo.ui.dCheckBox(self, Caption="Collapsed Panels To Bottom",
	            DataSource="self.Form.slideControl", DataField="CollapseToBottom")
		chkExpand = dabo.ui.dCheckBox(self, Caption="Expand Content to Full Size",
	            DataSource="self.Form.slideControl", DataField="ExpandContent")
		self.Sizer.appendSpacer(10)
		vsz = dabo.ui.dSizer("v")
		vsz.append(chkSingleton)
		vsz.append(chkSingle)
		vsz.append(chkBottom)
		vsz.append(chkExpand)
		hsz.append(vsz)
		self.Sizer.append(hsz, 0, halign="center", border=10)
		self.layout()


	def onBtn(self, evt):
		import random
		p = self.p1
		style = random.choice(p._barStyles)
		p.BarStyle = style
		color1 = dColors.randomColorName()
		color2 = dColors.randomColorName()
		p.BarColor1 = color1
		p.BarColor2 = color2
		if style in ("VerticalFill", "HorizontalFill"):
			p.Caption = "Style: %s; Colors: %s, %s" % (style, color1, color2)
		elif style in ("BorderOnly", ):
			p.Caption = "Style: %s" % style
		else:
			p.Caption = "Style: %s; Color: %s" % (style, color1)

	def onCollapseAll(self, evt):
		self.slideControl.collapseAll()

	def onExpandAll(self, evt):
		self.slideControl.expandAll()

			
if __name__ == "__main__":
	import test
	test.Test().runTest(_dSlidePanelControl_test)
