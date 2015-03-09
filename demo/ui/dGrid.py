# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dGrid
from dabo.ui import dColumn
from dabo import dColors

import datetime

class _dGrid_test(dGrid):
	def initProperties(self):
		thisYear = datetime.datetime.now().year
		tday = datetime.date.today()
		yday = tday-datetime.timedelta(days=1)
		ds = [
				{"name" : "Ed Leafe", "age" : thisYear - 1957, "coder" :  True, "color": "cornsilk", "date": tday},
				{"name" : "Paul McNett", "age" : thisYear - 1969, "coder" :	 True, "color": "wheat", "date": yday},
				{"name" : "Ted Roche", "age" : thisYear - 1958, "coder" :  True, "color": "goldenrod", "date": tday},
				{"name" : "Derek Jeter", "age": thisYear - 1974, "coder" :	False, "color": "white", "date": yday},
				{"name" : "Halle Berry", "age" : thisYear - 1966, "coder" :	 False, "color": "orange", "date": tday},
				{"name" : "Steve Wozniak", "age" : thisYear - 1950, "coder" :  True, "color": "yellow", "date": yday},
				{"name" : "LeBron James", "age" : thisYear - 1984, "coder" :  False, "color": "gold", "date": tday},
				{"name" : "Madeline Albright", "age" : thisYear - 1937, "coder" :  False, "color": "red", "date": yday}]


		for row in range(len(ds)):
			for i in range(20):
				ds[row]["i_%s" % i] = "sss%s" % i
		self.DataSet = ds

		self.TabNavigates = False
		self.Width = 360
		self.Height = 150
		self.Editable = False
		#self.Sortable = False
		#self.Searchable = False

	def afterInit(self):
		super(_dGrid_test, self).afterInit()

		# TODO: Phoenix has an issue with boolean columns
		if not dabo.ui.phoenix:
			self.addColumn(Name="Geek", DataField="coder", Caption="Geek?",
				Order=10, DataType="bool", Width=60, Sortable=False,
				Searchable=False, Editable=True, HeaderFontBold=False,
				HorizontalAlignment="Center", VerticalAlignment="Center",
				Resizable=False)

		col = dColumn(self, Name="Person", Order=20, DataField="name",
				DataType="string", Width=200, Caption="Celebrity Name",
				Sortable=True, Searchable=True, Editable=True, Expand=False)
		self.addColumn(col)

		col.HeaderFontItalic = True
		col.HeaderBackColor = "peachpuff"
		col.HeaderVerticalAlignment = "Top"
		col.HeaderHorizontalAlignment = "Left"

		# Let's make a custom editor for the name
		class ColoredText(dabo.ui.dTextBox):
			def initProperties(self):
				self.ForeColor = "blue"
				self.FontItalic = True
				self.FontSize = 24
			def onKeyChar(self, evt):
				self.ForeColor = dColors.randomColor()
				self.FontItalic = not self.FontItalic
		# Since we're using a big font, set a minimum height for the editor
		col.CustomEditorClass = dabo.ui.makeGridEditor(ColoredText, minHeight=40)

		# TODO: Phoenix has an issue with int columns
		if not dabo.ui.phoenix:
			self.addColumn(Name="Age", Order=30, DataField="age",
				DataType="integer", Width=40, Caption="Age",
				Sortable=True, Searchable=True, Editable=True)

		col = dColumn(self, Name="Color", Order=40, DataField="color",
				DataType="string", Width=40, Caption="Favorite Color",
				Sortable=True, Searchable=True, Editable=True, Expand=False)
		self.addColumn(col)

		# TODO: Phoenix has an issue with int columns
		if not dabo.ui.phoenix:
			col = dColumn(self, Name="Color", Order=40, DataField="date",
				          DataType="date", Width=40, Caption="Date",
				          Sortable=True, Searchable=True, Editable=True, Expand=False)
			self.addColumn(col)

		col.ListEditorChoices = dColors.colors
		col.CustomEditorClass = col.listEditorClass

		col.HeaderVerticalAlignment = "Bottom"
		col.HeaderHorizontalAlignment = "Right"
		col.HeaderForeColor = "brown"

		for i in range(1):
			# Can't test Expand with so many columns! Just add one.
			self.addColumn(DataField="i_%s" % i, Caption="i_%s" % i)

	def onScrollLineUp(self, evt):
		print("LINE UP orientation =", evt.orientation, " scrollpos =", evt.scrollpos)
	def onScrollLineDown(self, evt):
		print("LINE DOWN orientation =", evt.orientation, " scrollpos =", evt.scrollpos)
	def onScrollPageUp(self, evt):
		print("PAGE UP orientation =", evt.orientation, " scrollpos =", evt.scrollpos)
	def onScrollPageDown(self, evt):
		print("PAGE DOWN orientation =", evt.orientation, " scrollpos =", evt.scrollpos)
	def onScrollThumbDrag(self, evt):
		print("DRAG orientation =", evt.orientation, " scrollpos =", evt.scrollpos)
	def onScrollThumbRelease(self, evt):
		print("THUMB RELEASE orientation =", evt.orientation, " scrollpos =", evt.scrollpos)


class TestForm(dabo.ui.dForm):
	def afterInit(self):
		self.BackColor = "khaki"
		g = self.grid = _dGrid_test(self, RegID="sampleGrid")
		self.Sizer.append(g, 1, "x", border=0, borderSides="all")
		self.Sizer.appendSpacer(10)
		gsz = dabo.ui.dGridSizer(HGap=50)

		chk = dabo.ui.dCheckBox(self, Caption="Allow Editing?", RegID="gridEdit",
	            DataSource=self.grid, DataField="Editable")
		chk.update()
		gsz.append(chk, row=0, col=0)

		chk = dabo.ui.dCheckBox(self, Caption="Show Headers",
	            RegID="showHeaders", DataSource=self.grid,
	            DataField="ShowHeaders")
		gsz.append(chk, row=1, col=0)
		chk.update()

		chk = dabo.ui.dCheckBox(self, Caption="Allow Multiple Selection",
	            RegID="multiSelect", DataSource=self.grid,
	            DataField="MultipleSelection")
		chk.update()
		gsz.append(chk, row=2, col=0)

		chk = dabo.ui.dCheckBox(self, Caption="Vertical Headers",
	            RegID="verticalHeaders", DataSource=self.grid,
	            DataField="VerticalHeaders")
		chk.update()
		gsz.append(chk, row=3, col=0)

		chk = dabo.ui.dCheckBox(self, Caption="Auto-adjust Header Height",
	            RegID="autoAdjust", DataSource=self.grid,
	            DataField="AutoAdjustHeaderHeight")
		chk.update()
		gsz.append(chk, row=4, col=0)

		radSelect = dabo.ui.dRadioList(self, Choices=["Row", "Col", "Cell"],
	            ValueMode="string", Caption="Sel Mode", BackColor=self.BackColor,
	            DataSource=self.grid, DataField="SelectionMode", RegID="radSelect")
		radSelect.refresh()
		gsz.append(radSelect, row=0, col=1, rowSpan=3)

		def setVisible(evt):
			col = g.getColByDataField("name")
			but = evt.EventObject
			col.Visible = not col.Visible
			if col.Visible:
				but.Caption = "Make Celebrity Invisible"
			else:
				but.Caption = "Make Celebrity Visible"
		butVisible = dabo.ui.dButton(self, Caption="Toggle Celebrity Visibility",
	        OnHit=setVisible)
		gsz.append(butVisible, row=5, col=0)

		self.Sizer.append(gsz, halign="Center", border=10)
		gsz.setColExpand(True, 1)
		self.layout()

		self.fitToSizer(20, 20)

if __name__ == "__main__":
	from dabo.dApp import dApp
	app = dApp(MainFormClass=TestForm)
	app.setup()
	app.MainForm.radSelect.setFocus()
	app.start()
