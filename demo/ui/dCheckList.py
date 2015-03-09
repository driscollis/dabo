# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dCheckList
from dabo.dLocalize import _


class _dCheckList_test(dCheckList):
	def initProperties(self):
		# Simulate a database:
		actors = ({"lname": "Jason Leigh", "fname": "Jennifer", "iid": 42},
			{"lname": "Cates", "fname": "Phoebe", "iid": 23},
			{"lname": "Reinhold", "fname": "Judge", "iid": 13})

		choices = []
		keys = {}

		for actor in actors:
			choices.append("%s %s" % (actor['fname'], actor['lname']))
			keys[actor["iid"]] = len(choices) - 1

		self.Choices = choices
		self.Keys = keys
		self.ValueMode = 'Key'
		self.Value = 23

	def onHit(self, evt):
		print("HIT:")
		print("\tKeyValue: ", self.KeyValue)
		print("\tPositionValue: ", self.PositionValue)
		print("\tStringValue: ", self.StringValue)
		print("\tValue: ", self.Value)
		print("\tCount: ", self.Count)

	def onMouseLeftDoubleClick(self, evt):
		print("double click")

	def onMouseLeftDown(self, evt):
		print("mousedown")

if __name__ == "__main__":
	import test
	test.Test().runTest(_dCheckList_test)
