# -*- coding: utf-8 -*-
"""
Test Case for the dForm class.

If this file is run standalone, it will automatically run all of the test
cases found in the file.
"""
import unittest
import wtc
dui = wtc.dabo.ui
dabo = wtc.dabo

class Test_dForm(wtc.WidgetTestCaseWithDB):

	def testSomeSanityThings(self):
		frm = self.frm
		biz = frm.getBizobj()
		self.assertEqual(frm.cField.Value, "Paul Keith McNett")
		next(frm)
		frm.update(interval=0)  ## Need to force the update here which would otherwise happen 100 ms in the future.
		self.assertEqual(biz.RowNumber, 1)
		self.assertEqual(frm.cField.Value, "Edward Leafe")


	def testNullRecord(self):
		# This test currently fails (thanks John Fabiani for pointing it out). The
		# Dabo UI layer inappropriately converts None values into u"None" values.
		frm = self.frm
		biz = frm.getBizobj()
		self.createNullRecord()
		frm.requery()
		self.assertEqual(biz.RowCount, 4)
		frm.last()
		frm.update(interval=0)  ## Need to force the update here, otherwise it won't happen until 100 ms in the future.
		self.assertEqual(biz.RowNumber, 3)
		self.assertEqual(biz.Record.cField, None)
		self.assertEqual(biz.Record.iField, None)
		self.assertEqual(biz.Record.nField, None)

		self.assertEqual(frm.cField.Value, None)
		self.assertEqual(frm.iField.Value, None)
		self.assertEqual(frm.nField.Value, None)


if __name__ == "__main__":
	unittest.main()
