# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dLabel
from dabo.ui import dForm


class _dLabel_test(dLabel):
	def initProperties(self):
		self.FontBold = True
		self.Alignment = "Center"
		self.ForeColor = "Red"
		self.Width = 300
		self.Caption = "My God, it's full of stars! " * 22
		self.WordWrap = False


if __name__ == "__main__":
	from dabo.dApp import dApp
	class LabelTestForm(dForm):
		def afterInit(self):
			self.Caption = "dLabel Test"
			pnl = dabo.ui.dPanel(self)
			self.Sizer.append1x(pnl)
			sz = pnl.Sizer = dabo.ui.dSizer("v")
			sz.appendSpacer(25)
			self.sampleLabel = dabo.ui.dLabel(pnl, Caption="This label has a very long Caption. " * 20,
					WordWrap=False)
			self.wrapControl = dabo.ui.dCheckBox(pnl, Caption="WordWrap",
					DataSource=self.sampleLabel, DataField="WordWrap")
			sz.append(self.wrapControl, halign="center", border=20)
			sz.append1x(self.sampleLabel, border=10)
			self.update()
			dabo.ui.callAfterInterval(200, self.layout)

	app = dApp(MainFormClass=LabelTestForm)
	app.start()
