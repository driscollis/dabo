# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dForm
from dabo.ui import dBorderlessForm

from dabo import dEvents
from dabo.dLocalize import _


class _dForm_test(dForm):
	def afterInit(self):
		self.Caption = _("Regular Form")
	def onActivate(self, evt):
		print(_("Activate"))
	def onDeactivate(self, evt):
		print(_("Deactivate"))


class _dBorderlessForm_test(dBorderlessForm):
	def afterInit(self):
		self.btn = dabo.ui.dButton(self, Caption=_("Close Borderless Form"))
		self.Sizer.append(self.btn, halign="Center", valign="middle")
		self.layout()
		self.btn.bindEvent(dEvents.Hit, self.close)
		dabo.ui.callAfter(self.setSize)

	def setSize(self):
		self.Width, self.Height = self.btn.Width + 60, self.btn.Height + 60
		self.layout()
		self.Centered = True


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dForm_test)
	test.Test().runTest(_dBorderlessForm_test)

