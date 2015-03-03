"""
Test Case for the dTextbox class.

If this file is run standalone, it will automatically run all of the test
cases found in the file.
"""

import unittest
import wtc
dui = wtc.dabo.ui
dabo = wtc.dabo

import datetime
import decimal
from six import string_types as sixBasestring


class TestTextLengthProperty(wtc.WidgetTestCase):
	"""
	Test List:
		- Set TextLength to n.  TextLength should be equal to n. (round trip test)
		- setting TextLength should fail with a value that can't be converted to an int
		- Set TextLength to n.  Value should remain the same if < n
		- Set TextLength to n.  Value should remain the same if = n
		- Set TextLength to n.  Value should now be dTextBox.Value[:n] if > n
		- setting TextLength to a negative number should fail.
		- setting TextLength to None should allow any length
		- setting TextLength to Zero should fail.
		- TextLength = n.  Set Value to string with length > n should set only string[:n].
	"""
	
	def testRoundTrip(self):
		"""Set TextLength to n.  TextLength should be equal to n. (round trip test)"""
		self.testTextBox = dui.dTextBox(self.form)
		for x in range(1, 15):
			self.testTextBox.TextLength = x
			self.assertEqual(self.testTextBox.TextLength, x)
			self.testTextBox.TextLength = str(x)
			self.assertEqual(self.testTextBox.TextLength, x)
	
	def testNonIntegerInput(self):
		"""setting TextLength should fail with a value that can't be converted to an int"""
		self.testTextBox = dui.dTextBox(self.form)
		self.assertRaises(ValueError, self.setProperty, ("self.testTextBox.TextLength", '"not a number"'))
		self.assertRaises(TypeError, self.setProperty, ("self.testTextBox.TextLength", "(234, 543, 'ho hum')"))
	
	def testValueLessThanLength(self):
		"""Set TextLength to n.  Value should remain the same if < n"""
		self.testTextBox = dui.dTextBox(self.form)
		self.testTextBox.Value = "Length is 12"
		self.testTextBox.TextLength = 13
		self.assertEqual(self.testTextBox.Value, "Length is 12")
	
	def testValueEqualToLength(self):
		"""Set TextLength to n.  Value should remain the same if = n"""
		self.testTextBox = dui.dTextBox(self.form)
		self.testTextBox.Value = "Length is 12"
		self.testTextBox.TextLength = 12
		self.assertEqual(self.testTextBox.Value, "Length is 12")
	
	def testValueGreaterThanLength(self):
		"""Set TextLength to n.  Value should now be dTextBox.Value[:n] if > n"""
		self.testTextBox = dui.dTextBox(self.form)
		self.testTextBox.Value = "Length is 12"
		self.testTextBox.TextLength = 11
		self.assertEqual(self.testTextBox.Value, "Length is 1")
	
	def testFailOnNegativeInput(self):
		"""setting TextLength to a negative number should fail."""
		self.testTextBox = dui.dTextBox(self.form)
		self.assertRaises(ValueError, self.setProperty, ("self.testTextBox.TextLength", "-1"))
	
	def testNoneIsAnyLength(self):
		"""setting TextLength to None should allow any length"""
		self.testTextBox = dui.dTextBox(self.form)
		self.testTextBox.TextLength = None
		self.testTextBox.Value = "aaaaa"*100
		self.assertEqual(self.testTextBox.Value, "aaaaa"*100)
	
	def testFailOnZeroInput(self):
		"""setting TextLength to Zero should fail."""
		self.testTextBox = dui.dTextBox(self.form)
		self.assertRaises(ValueError, self.setProperty, ("self.testTextBox.TextLength", "-0"))
	
	def testNoInsertionUponLimitReached(self):
		"""extLength = n.  Set Value to string with length > n should set only string[:n]."""
		self.testTextBox = dui.dTextBox(self.form)
		self.testTextBox.TextLength = 4
		self.testTextBox.Value = "Value"
		self.assertEqual(self.testTextBox.Value, "Value")


class Test_dTextBox(wtc.WidgetTestCase):

	def mockUserInput(self, str_val, lose_focus=True):
		txt = self.txt
		txt._gotFocus()
		txt.SetValue(str_val)
		if lose_focus:
			txt._lostFocus()

	def testStringValue(self):
		self.txt = self.form.addObject(dui.dTextBox)
		txt = self.txt
		txt.Value = "This is a string"
		self.assertTrue(isinstance(txt.Value, sixBasestring))
		self.assertEqual(txt.Value, "This is a string")
		self.mockUserInput("23")
		self.assertTrue(isinstance(txt.Value, sixBasestring))
		self.assertEqual(txt.Value, "23")
		txt.Value = None
		self.assertEqual(txt.Value, None)
		self.mockUserInput("hi there")
		self.assertEqual(txt.Value, "hi there")

	def testFloatValue(self):
		self.txt = self.form.addObject(dui.dTextBox)
		txt = self.txt
		txt.Value = 1.23
		self.assertTrue(isinstance(txt.Value, float))
		self.assertEqual(txt.Value, 1.23)
		self.mockUserInput("23")
		self.assertTrue(isinstance(txt.Value, float))
		self.assertEqual(txt.Value, 23)
		txt.Value = None
		self.assertEqual(txt.Value, None)
		self.mockUserInput("hi there")
		self.assertEqual(txt.Value, None)
		self.mockUserInput("42")
		self.assertEqual(txt.Value, 42)
		self.assertTrue(isinstance(txt.Value, float))


	def testIntValue(self):
		self.txt = self.form.addObject(dui.dTextBox)
		txt = self.txt
		txt.Value = 23
		self.assertTrue(isinstance(txt.Value, int))
		self.assertEqual(txt.Value, 23)
		self.mockUserInput("323.75")
		self.assertTrue(isinstance(txt.Value, int))
		self.assertEqual(txt.Value, 23)
		txt.Value = None
		self.assertEqual(txt.Value, None)
		self.mockUserInput("hi there")
		self.assertEqual(txt.Value, None)
		self.mockUserInput("42")
		self.assertEqual(txt.Value, 42)
		self.assertTrue(isinstance(txt.Value, int))

	def testDateValue(self):
		self.txt = self.form.addObject(dui.dTextBox)
		txt = self.txt
		txt.Value = datetime.date.today()
		self.assertTrue(isinstance(txt.Value, datetime.date))
		self.assertEqual(txt.Value, datetime.date.today())
		self.mockUserInput("2006-05-03")
		self.assertTrue(isinstance(txt.Value, datetime.date))
		self.assertEqual(txt.Value, datetime.date(2006, 5, 3))
		txt.Value = None
		self.assertEqual(txt.Value, None)
		self.mockUserInput("hi there")
		self.assertEqual(txt.Value, None)
		self.mockUserInput("2006-05-03")
		self.assertEqual(txt.Value, datetime.date(2006, 5, 3))

	def testDateTimeValue(self):
		self.txt = self.form.addObject(dui.dTextBox)
		txt = self.txt
		txt.Value = val = datetime.datetime.now()
		self.assertTrue(isinstance(txt.Value, datetime.datetime))
		# microseconds are not equal, sould we use val.ctime() for comp???
		self.assertEqual(txt.Value, val)
		self.mockUserInput("bogus datetime")
		self.assertTrue(isinstance(txt.Value, datetime.datetime))
		self.assertEqual(txt.Value, val)
		txt.Value = None
		self.assertEqual(txt.Value, None)

	def testDecimalValue(self):
		self.txt = self.form.addObject(dui.dTextBox)
		txt = self.txt
		txt.Value = decimal.Decimal("1.23")
		self.assertTrue(isinstance(txt.Value, decimal.Decimal))
		self.assertEqual(txt.Value, decimal.Decimal("1.23"))
		self.mockUserInput("15badinput")
		self.assertTrue(isinstance(txt.Value, decimal.Decimal))
		self.assertEqual(txt.Value, decimal.Decimal("1.23"))
		txt.Value = None
		self.assertEqual(txt.Value, None)
		self.mockUserInput("hi there")
		self.assertEqual(txt.Value, None)
		self.mockUserInput("42.23")
		self.assertEqual(txt.Value, decimal.Decimal("42.23"))
		self.assertTrue(isinstance(txt.Value, decimal.Decimal))

	def testFlushValue(self):
		self.txt = self.form.addObject(dui.dTextBox)
		txt = self.txt
		txt.Form.df = None

		txt.DataSource = "form"
		txt.DataField = "df"
		txt.Value = "Paul"
		self.assertEqual(txt.Value, "Paul")
		self.assertEqual(txt.Value, txt.Form.df)

		self.mockUserInput("kk")
		self.assertEqual(txt.Value, "kk")

		self.mockUserInput("pp", lose_focus=False)
		self.assertEqual(txt.Value, "pp")
		self.assertEqual(txt.Form.df, "kk")
		txt.flushValue()
		self.assertEqual(txt.Form.df, "pp")
		self.assertEqual(txt.Value, "pp")

if __name__ == "__main__":
	unittest.main()
