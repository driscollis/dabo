# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dRadioList


class _dRadioList_test(dRadioList):
	def afterInit(self):
		self.Caption = "Developers"
		self.BackColor = "lightyellow"
		developers = [{"lname": "McNett", "fname": "Paul", "iid": 42},
				{"lname": "Leafe", "fname": "Ed", "iid": 23},
				{"lname": "Roche", "fname": "Ted", "iid": 11}]

		self.Choices = ["%s %s" % (dev["fname"], dev["lname"]) for dev in developers]
		developers.append({"lname": "Hentzen", "fname": "Whil", "iid": 93})
		self.Choices = ["%s %s" % (dev["fname"], dev["lname"]) for dev in developers]
		keys = [dev["iid"] for dev in developers]
		self.Keys = keys
		self.ValueMode = "key"


	def onHit(self, evt):
		print("KeyValue: ", self.KeyValue)
		print("PositionValue: ", self.PositionValue)
		print("StringValue: ", self.StringValue)
		print("Value: ", self.Value)



if __name__ == "__main__":
	import test
	test.Test().runTest(_dRadioList_test)
