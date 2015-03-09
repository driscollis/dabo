# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dComboBox
from dabo.dLocalize import _


class _dComboBox_test(dComboBox):
	def initProperties(self):
		self.setup()
		self.AppendOnEnter = True


	def setup(self):
		# Simulating a database:
		wannabeCowboys = ({"lname": "Reagan", "fname": "Ronald", "iid": 42},
			{"lname": "Bush", "fname": "George W.", "iid": 23})

		choices = []
		keys = {}
		for wannabe in wannabeCowboys:
			choices.append("%s %s" % (wannabe['fname'], wannabe['lname']))
			keys[wannabe["iid"]] = len(choices) - 1

		self.Choices = choices
		self.Keys = keys
		self.ValueMode = 'key'


	def beforeAppendOnEnter(self):
		txt = self._textToAppend.strip().lower()
		if txt == "dabo":
			print(_("Attempted to add Dabo to the list!!!"))
			return False
		elif txt.find("nixon") > -1:
			self._textToAppend = "Tricky Dick"


	def onHit(self, evt):
		print("KeyValue: ", self.KeyValue)
		print("PositionValue: ", self.PositionValue)
		print("StringValue: ", self.StringValue)
		print("Value: ", self.Value)
		print("UserValue: ", self.UserValue)


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dComboBox_test)
