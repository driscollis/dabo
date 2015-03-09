# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dLed
from dabo import dColors


class TestForm(dabo.ui.dForm):
	def afterInit(self):
		mp = dabo.ui.dPanel(self)
		self.Sizer.append1x(mp)
		mp.Sizer = dabo.ui.dSizer("h")
		led = dLed(mp, RegID="LED")
		mp.Sizer.append(led, proportion=4, layout='expand')

		vs = dabo.ui.dSizer("v", DefaultBorder=20)
		vs.appendSpacer(20)
		vs.DefaultBorderLeft = vs.DefaultBorderRight = True
		btn = dabo.ui.dToggleButton(mp, Caption="Toggle LED",
	            DataSource=self.LED, DataField="On", Value=False)
		vs.append(btn)
		vs.appendSpacer(12)
		vs.append(dabo.ui.dLabel(mp, Caption="On Color:"))
		dd = dabo.ui.dDropdownList(mp, Choices=dColors.colors,
	            DataSource=self.LED, DataField="OnColor", Value="mediumseagreen")
		vs.append(dd)
		vs.appendSpacer(12)
		vs.append(dabo.ui.dLabel(mp, Caption="Off Color:"))
		dd = dabo.ui.dDropdownList(mp, Choices=dColors.colors,
	            DataSource=self.LED, DataField="OffColor", Value="orangered")
		vs.append(dd)
		mp.Sizer.append(vs)
		
		self.LED.On = True
		self.update()

			
if __name__ == '__main__':
	from dabo.dApp import dApp
	app = dApp()
	app.MainFormClass = TestForm
	app.start()
