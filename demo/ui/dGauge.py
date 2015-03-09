# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dGauge
from dabo.ui import dEvents


class _dGauge_test(dGauge):
	def afterInit(self):
		self._timer = dabo.ui.dTimer()
		self._timer.bindEvent(dEvents.Hit, self.onTimer)
		self._timer.Interval = 23
		self._timer.start()

	def initProperties(self):
		self.Range = 1000
		self.Value = 0
		self.Width = 300

	def onTimer(self, evt):
		if not self:
			return
		if self.Value < self.Range:
			self.Value += 1
		else:
			self._timer.stop()
			self.Value = 0
			self._timer.start()


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dGauge_test)
