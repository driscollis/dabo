# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dListBox


class _dListBox_test(dListBox):
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

#		self.MultipleSelect = True
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
		print("double click at position %s" % self.PositionValue)

	def onMouseLeftDown(self, evt):
		print("mousedown")

if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dListBox_test)

