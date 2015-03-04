# -*- coding: utf-8 -*-
"""
Test Case for the dEditBox class.

If this file is run standalone, it will automatically run all of the test
cases found in the file.
"""

import unittest
import wtc
dui = wtc.dabo.ui
dabo = wtc.dabo

from six import string_types as sixBasestring


class Test_dEditBox(wtc.WidgetTestCase):

	def testValue(self):
		self.edt = self.form.addObject(dui.dEditBox)
		edt = self.txt = self.edt
		edt.Value = "This is a string"
		self.assertTrue(isinstance(edt.Value, sixBasestring))
		self.assertEqual(edt.Value, "This is a string")
		self.mockUserInput("23")
		self.assertTrue(isinstance(edt.Value, sixBasestring))
		self.assertEqual(edt.Value, "23")
		edt.Value = None
		self.assertEqual(edt.Value, None)
		self.mockUserInput("hi there")
		self.assertEqual(edt.Value, "hi there")


if __name__ == "__main__":
	unittest.main()
