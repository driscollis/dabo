# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dSlider


class _dSlider_test(dSlider):
	def initProperties(self):
		self.Size = (300, 300)
		self.Max = 95
		self.Min = 23
		self.Value = 75
		self.ShowLabels = True
		# Try changing these to see their effects
# 		self.Reversed = True
#  		self.TickPosition = "Left"

	def onHit(self, evt):
		print("Hit! Value =", self.Value)


if __name__ == "__main__":
	import test
	test.Test().runTest(_dSlider_test)
