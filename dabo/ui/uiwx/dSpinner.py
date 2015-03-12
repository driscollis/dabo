# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dSpinner


class _dSpinner_test(dSpinner):
	def initProperties(self):
		self.Max = 55
		self.Min = 0
		self.Value = 0
		self.Increment = 8.75
		self.SpinnerWrap = True
		self.FontSize = 10
		self.Width = 80

	def onHit(self, evt):
		print("HIT!", self.Value, "Hit Type", evt.hitType)

	def onValueChanged(self, evt):
		print("Value Changed", self.Value)
		print("___")

	def onInteractiveChange(self, evt):
		print("Interactive Change", self.Value)

	def onSpinUp(self, evt):
		print("Spin up event.")

	def onSpinDown(self, evt):
		print("Spin down event.")

	def onSpinner(self, evt):
		print("Spinner event.")


if __name__ == "__main__":
	import test
	test.Test().runTest(_dSpinner_test)
