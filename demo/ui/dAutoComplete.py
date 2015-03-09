# -*- coding: utf-8 -*-
import dabo.ui

if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dAutoComplete


class _dAutoComplete_test(dabo.ui.dPanel):
	def afterInit(self):
		import datetime
		currentYear = datetime.datetime.now().year
		self.Caption = "dAutoComplete"
		self.Sizer = vs = dabo.ui.dSizer("v")
		ds = [{"landmark":"Eiffel Tower", "loc":"Paris, France", "constructed":"1889"},
	            {"landmark":"Statue of Liberty", "loc":"New York, New York", "constructed":"1884"},
	            {"landmark":"Great Sphinx of Giza", "loc":"Giza, Egypt", "constructed":"c. 2558 BC"},
	            {"landmark":"Stonehenge", "loc":"Wiltshire, England", "constructed":"3000 - 2000 BC"}]

		vs.append(dabo.ui.dLabel(self, Caption="Press the down arrow key to see the list of choices.",
	            FontBold=True), alignment="center")
		vs.appendSpacer(15)
		vs.append(dabo.ui.dLabel(self, Caption="User defined choices (single-column)"))
		vs.append(dAutoComplete(self, Choices=["Bob", "Joe", "Mary", "Bill", "Marcia", "Eric"]), "x")
		vs.appendSpacer(5)
		vs.append(dabo.ui.dLabel(self, Caption="Data set (single-column)"))
		vs.append(dAutoComplete(self, DataSet=ds, DataFields=["landmark"]), "x")
		vs.appendSpacer(5)
		vs.append(dabo.ui.dLabel(self, Caption="Data set (multi-column):"))
		vs.append(dAutoComplete(self, DataSet=ds, SearchField="landmark", FetchField="loc",
	            ColNames=["Landmark", "Location", "Year Constructed"]), "x")


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dAutoComplete_test)
