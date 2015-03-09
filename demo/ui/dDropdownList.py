# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dDropdownList

from dabo.dLocalize import _


class _dDropdownList_test(dDropdownList):
	def initProperties(self):
		# Simulating a database
		developers = ({"lname": "McNett", "fname": "Paul", "iid": 42},
			{"lname": "Leafe", "fname": "Ed", "iid": 23})

		choices = []
		keys = {}
		for developer in developers:
			choices.append("%s %s" % (developer['fname'], developer['lname']))
			keys[developer["iid"]] = len(choices) - 1

		self.Choices = choices
		self.Keys = keys
		self.ValueMode = "key"


	def onValueChanged(self, evt):
		print("KeyValue: ", self.KeyValue)
		print("PositionValue: ", self.PositionValue)
		print("StringValue: ", self.StringValue)
		print("Value: ", self.Value)


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dDropdownList_test)
