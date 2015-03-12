# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dPanel
from dabo.ui import dTimer

from dabo import dEvents


class _dTimer_skip(dPanel):
	def afterInit(self):
		# Only setting this so that the test Caption is correct
		self._baseClass = dTimer
		self.fastTimer = dTimer(self, Interval=500)
		self.fastTimer.bindEvent(dEvents.Hit, self.onFastTimerHit)
		self.slowTimer = dTimer(Interval=2000)
		self.slowTimer.bindEvent(dEvents.Hit, self.onSlowTimerHit)
		self.fastTimer.start()
		self.slowTimer.start()

	def onFastTimerHit(self, evt):
		print("fast timer fired!")

	def onSlowTimerHit(self, evt):
		print("slow timer fired!")


if __name__ == "__main__":
	import test
	test.Test().runTest(_dTimer_skip)
