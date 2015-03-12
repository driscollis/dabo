# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dSearchBox
from dabo.ui import textboxmixin as tbm
from dabo.dLocalize import _
import dabo.dEvents as dEvents
from dabo.ui import makeDynamicProperty

import datetime


# This test sets up several textboxes, each editing different data types.
class TestBase(dSearchBox):
	def initProperties(self):
		super(TestBase, self).initProperties()
		self.LogEvents = ["ValueChanged", "searchButtonClicked", "SearchCancelButtonClicked"]
		self.CancelButtonVisible = True
		self.SearchButtonVisible = True
		self.List = ("item 1", "item 2", "item 3")

	def onValueChanged(self, evt):
		if self.IsSecret:
			print("%s changed, but the new value is a secret!" % self.Name)
		else:
			print("%s.onValueChanged:" % self.Name, self.Value, type(self.Value))

	def onSearchButtonClicked(self, evt):
		print("you pressed the search button")

	def onSearchCancelButtonClicked(self, evt):
		print("you pressed the cancel button")


class IntText(TestBase):
	def afterInit(self):
		self.Value = 23

class FloatText(TestBase):
	def afterInit(self):
		self.Value = 23.5
		self.List = ['changed item 1', 'changed item 2']

class BoolText(TestBase):
	def afterInit(self):
		self.Value = False

# have at least one for the test.py all test
class _dSearchBox_test(TestBase):
	def afterInit(self):
		self.Value = "Lunchtime"

class PWText(TestBase):
	def __init__(self, *args, **kwargs):
		kwargs["PasswordEntry"] = True
		super(PWText, self).__init__(*args, **kwargs)
	def afterInit(self):
		self.Value = "TopSecret!"

class DateText(TestBase):
	def afterInit(self):
		self.Value = datetime.date.today()
		self.List = ['historyItem 1', 'historyItem 2']

class DateTimeText(TestBase):
	def afterInit(self):
		self.Value = datetime.datetime.now()

testParms = [IntText, FloatText, _dSearchBox_test, PWText, BoolText, DateText, DateTimeText]

import decimal

class DecimalText(TestBase):
	def afterInit(self):
		self.Value = decimal.Decimal("23.42")

			
if __name__ == "__main__":
	import test
	testParms.append(DecimalText)
	test.Test().runTest(testParms)
