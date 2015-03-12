# -*- coding: utf-8 -*-
import six
if six.PY2:
	sixLong = long
else:
	sixLong = int
	
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dTextBox

import datetime
import decimal

# This test sets up several textboxes, each editing different data types.
class TestBase(dTextBox):
	def initProperties(self):
		self.SelectOnEntry = True
		super(TestBase, self).initProperties()
		self.LogEvents = ["ValueChanged",]

	def onValueChanged(self, evt):
		if self.IsSecret:
			print("%s changed, but the new value is a secret! " % self.Name)
		else:
			print("%s.onValueChanged:" % self.Name, self.Value, type(self.Value))

class IntText(TestBase):
	def afterInit(self):
		self.Value = 23

class LongText(TestBase):
	def afterInit(self):
		self.Value = sixLong(23)

class FloatText(TestBase):
	def afterInit(self):
		self.Value = 23.5

class BoolText(TestBase):
	def afterInit(self):
		self.Value = False

class _dTextBox_Test(TestBase):
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

class DateTimeText(TestBase):
	def afterInit(self):
		self.Value = datetime.datetime.now()

testParms = [IntText, LongText, FloatText, _dTextBox_Test, PWText, BoolText, DateText, DateTimeText]

try:
	import mx.DateTime
	class MxDateTimeText(TestBase):
		def afterInit(self):
			self.Value = mx.DateTime.now()

	testParms.append(MxDateTimeText)
except ImportError:
	# skip it: mx may not be available
	pass

class DecimalText(TestBase):
	def afterInit(self):
		self.Value = decimal.Decimal("23.42")

testParms.append(DecimalText)

if __name__ == "__main__":
	import test
	test.Test().runTest(testParms)
