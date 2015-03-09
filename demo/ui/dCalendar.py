# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dForm
from dabo.ui import dCalendar
from dabo.ui import dExtendedCalendar

from dabo.dLocalize import _


class _dCalendar_test(dForm):
	def afterInit(self):
		dCalendar(self, FirstDayOfWeek="monday",
	            Position=(0, 0), RegID="cal")
		self.cal.HighlightHolidays = True
		self.cal.setHolidays(((None, 12, 25), (2006, 1, 4)))

		dExtendedCalendar(self, FirstDayOfWeek="monday",
	            Position=(0, 0), RegID="extCal")

		self.Sizer.append(self.cal, halign="Center", valign="middle")
		self.Sizer.append(self.extCal, halign="Center", valign="middle")
		self.layout()

	def onCalendarDayHeaderClicked_cal(self, evt):
		print("Day of week:", evt.weekday)
	def onCalendarDateChanged_cal(self, evt):
		print("DateChanged!", evt.date)
	def onCalendarDayChanged_cal(self, evt):
		print("DayChanged!", evt.date)
	def onCalendarMonthChanged_cal(self, evt):
		print("MonthChanged!", evt.date)
	def onCalendarYearChanged_cal(self, evt):
		print("YearChanged!", evt.date)
	def onHit_cal(self, evt):
		print("Hit!", evt.date)
		self.release()


			
if __name__ == "__main__":
	from dabo.dApp import dApp

	app = dApp()
	app.MainFormClass = _dCalendar_test
	app.start()



