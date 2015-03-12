#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO: Robin hasn't converted richtext completely, i.e. RichTextXMLHandler
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dForm
from dabo.ui import dRichTextBox

from dabo.dLocalize import _
from dabo.lib.utils import ustr


class RichTextTestForm(dabo.ui.dForm):
	def initProperties(self):
		self.ShowToolBar = True
		self.Caption = "Rich Text Control"

	def afterInitAll(self):
		self.textControl = dRichTextBox(self)
		self.textControl.Value = self.getDummyText()
		self.Sizer.append1x(self.textControl)
		self._currentDefaultStyle = None
		iconPath = "themes/tango/32x32/actions"
		self.tbbBold = self.appendToolBarButton("Bold", pic="%s/format-text-bold" % iconPath,
				toggle=True, help="Toggle the Bold style of the selected text", tip="Bold",
				OnHit=self.toggleStyle)
		self.tbbItalic = self.appendToolBarButton("Italic", pic="%s/format-text-italic" % iconPath,
				toggle=True, help="Toggle the Italic style of the selected text", tip="Italic",
				OnHit=self.toggleStyle)
		self.tbbUnderline = self.appendToolBarButton("Underline",
				pic="%s/format-text-underline" % iconPath, toggle=True,
				help="Toggle the Underline style of the selected text", tip="Underline",
				OnHit=self.toggleStyle)
		tb = self.ToolBar
		allfonts = dabo.ui.getAvailableFonts()
		# This is necessary because wx reports the font in some cases as 'applicationfont'.
		allfonts.append("applicationfont")
		allfonts.sort()
		self.tbFontFace = dabo.ui.dDropdownList(tb, Caption="FontFace",
				ValueMode="String", OnHit=self.onSetFontFace,
				Choices=allfonts)
		tb.appendControl(self.tbFontFace)
		self.tbFontSize = dabo.ui.dDropdownList(tb, Caption="FontSize",
				ValueMode="String", OnHit=self.onSetFontSize)
		self.tbFontSize.Choices = [ustr(i) for i in range(6, 129)]

		# Tried a spinner, but this doesn't work in toolbars.
# 		self.tbFontSize = dabo.ui.dSpinner(tb,
# 				Min=7, Max=128, OnHit=self.onSetFontSize)

		tb.appendControl(self.tbFontSize)

		self.tbBackColor = dabo.ui.dToggleButton(tb, Caption="BackColor", FontSize=8,
				Size=(54, 32), OnHit=self.onSetBackColor, BezelWidth=0, Value=True)
		tb.appendControl(self.tbBackColor)
		self.tbForeColor = dabo.ui.dToggleButton(tb, Caption="ForeColor", FontSize=8,
				Size=(54, 32), OnHit=self.onSetForeColor, BezelWidth=0, Value=True)
		tb.appendControl(self.tbForeColor)
		self.openButton = dabo.ui.dButton(tb, Caption="Open", OnHit=self.onOpen)
		tb.appendControl(self.openButton)
		self.saveButton = dabo.ui.dButton(tb, Caption="Save", OnHit=self.onSave)
		tb.appendControl(self.saveButton)
		self.styleTimer = dabo.ui.dTimer(self, Interval=500, Enabled=True,
				OnHit=self.checkForUpdate)

		# For development: uncomment the next line, and add the code you want to
		# run to the onTest() method.
# 		btn = tb.appendControl(dabo.ui.dButton(tb, Caption="TEST", OnHit=self.onTest))


	def onTest(self, evt):
		pass

	def onOpen(self, evt):
		self.textControl.load()

	def onSave(self, evt):
		self.textControl.save()

	def onSetFontSize(self, evt):
		if self.textControl.SelectionRange == (None, None):
			# No selection; revert the dropdown value
			self.updateSelection()
			return
		self.textControl.SelectionFontSize = int(evt.EventObject.Value)

	def onSetFontFace(self, evt):
		if self.textControl.SelectionRange == (None, None):
			# No selection; revert the dropdown value
			self.updateSelection()
			return
		self.textControl.SelectionFontFace = evt.EventObject.Value

	def onSetBackColor(self, evt):
		self.tbBackColor.Value = True
		curr = self.textControl.SelectionBackColor
		if curr is None:
			# Nothing selected
			return
		newcolor = dabo.ui.getColor(curr)
		if newcolor:
			self.textControl.SelectionBackColor = newcolor

	def onSetForeColor(self, evt):
		self.tbForeColor.Value = True
		curr = self.textControl.SelectionForeColor
		if curr is None:
			# Nothing selected
			return
		newcolor = dabo.ui.getColor(curr)
		if newcolor:
			self.textControl.SelectionForeColor = newcolor

	def toggleStyle(self, evt):
		obj = evt.EventObject
		tx = self.textControl
		cap = obj.Caption
		if cap == "Bold":
			tx.SelectionFontBold = not tx.SelectionFontBold
		elif cap == "Italic":
			tx.SelectionFontItalic = not tx.SelectionFontItalic
		elif cap == "Underline":
			tx.SelectionFontUnderline = not tx.SelectionFontUnderline

	def getCurrentStyle(self):
		tx = self.textControl
		bc = tx.CurrentBackColor
		fc = tx.CurrentForeColor
		cff = tx.CurrentFontFace
		cfs = tx.CurrentFontSize
		cfb = tx.CurrentFontBold
		cfi = tx.CurrentFontItalic
		cfu = tx.CurrentFontUnderline
		return (cff, cfs, cfb, cfi, cfu, bc, fc)

	def checkForUpdate(self, evt):
		style = self.getCurrentStyle()
		if style != self._currentDefaultStyle:
			self._currentDefaultStyle = style
			self.updateSelection(style)

	def updateSelection(self, style=None):
		if style is None:
			style = self.getCurrentStyle()
		cff, cfs, cfb, cfi, cfu, bc, fc = style
		self.tbFontFace.Value = cff
		self.tbFontSize.Value = ustr(cfs)
		self.tbbBold.Value = cfb
		self.tbbItalic.Value = cfi
		self.tbbUnderline.Value = cfu
		self.tbBackColor.BackColor = bc
		self.tbForeColor.BackColor = fc

	def getDummyText(self):
		return """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi.

Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus.

Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc.
"""



if __name__ == "__main__":
	import test
	test.Test().runTest(RichTextTestForm)

