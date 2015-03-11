# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dMaskedTextBox
from dabo.dLocalize import _

import datetime


class _dMaskedTextBox_test(dabo.ui.dForm):
	def afterInit(self):
		self.Caption = "dMaskedTextBox"
		pgf = dabo.ui.dPageFrame(self, TabPosition="Left", PageCount=3)
		self.Sizer.append1x(pgf, border=20)
		pg1, pg2, pg3 = pgf.Pages
		pg1.Caption = "Basic Masks"
		pg2.Caption = "Pre-defined Formats"
		pg3.Caption = "Input Codes"

		sz = pg1.Sizer = dabo.ui.dGridSizer(MaxCols=2, HGap=5, VGap=5)

		lbl = dabo.ui.dLabel(pg1, Caption="Basic Masks")
		lbl.FontSize += 2
		sz.append(lbl, colSpan=2, halign="center")
		"""The below code does not work in some versions of wxPython because of a bug discovered
			in wxPython 2.8.9.1 maskededit.py.  If you find that you have such a version, either upgrade
			to a newer wxPython, or you can fix it in your own wx code. Find the line in
			'lib/masked/maskededit.py' that reads:
			'if field._forcelower and key in range(97,123):'
			and replace it with
			'if field._forcelower and key in range(65,90):'  """
		sz.append(dabo.ui.dLabel(pg1, Caption="""Forced Lowercase Letters Only:
(May not work in older
versions of wxPython)"""), halign="right")
		sz.append(dMaskedTextBox(pg1, Width=240, InputCodes='^', Mask="C{20}"), valign="Top")

		sz.append(dabo.ui.dLabel(pg1, Caption="Accepts Uppercase Letters Only:"), halign="right")
		sz.append(dMaskedTextBox(pg1, Width=240, Mask="A{20}"))

		sz.append(dabo.ui.dLabel(pg1, Caption="Forced Uppercase Letters Only:"), halign="right")
		sz.append(dMaskedTextBox(pg1, Width=240, InputCodes='!>', Mask="C{20}"))

		sz.append(dabo.ui.dLabel(pg1, Caption="Lowercase Letters Only:"), halign="right")
		sz.append(dMaskedTextBox(pg1, Width=240, Mask="a{20}"))

		sz.append(dabo.ui.dLabel(pg1, Caption="Letters (any case) Only:"), halign="right")
		sz.append(dMaskedTextBox(pg1, Width=240, Mask="C{20}"))

		sz.append(dabo.ui.dLabel(pg1, Caption="Punctuation Only:"), halign="right")
		sz.append(dMaskedTextBox(pg1, Width=240, Mask="&{20}"))

		sz.append(dabo.ui.dLabel(pg1, Caption="Letter left; Numbers right:"), halign="right")
		sz.append(dMaskedTextBox(pg1, Width=240, Mask="C{6} - #{6}"))

		sz.append(dabo.ui.dLabel(pg1, Caption="No Mask:"), halign="right")
		sz.append(dMaskedTextBox(pg1, Width=240, Mask=""))
		lbl = dabo.ui.dLabel(pg1, FontItalic=True,
		                     Caption="The 'No Mask' value can never be valid,\nand will be cleared when the control loses focus.")
		lbl.FontSize -= 2
		sz.append(lbl, colSpan=2, halign="center")
		sz.setColExpand(1, True)

		sz = pg2.Sizer = dabo.ui.dGridSizer(MaxCols=2, HGap=5, VGap=5)

		lbl = dabo.ui.dLabel(pg2, Caption="Pre-defined Formats")
		lbl.FontSize += 2
		sz.append(lbl, colSpan=2, halign="center")

		fmts = dMaskedTextBox.getFormats()
		fmts.sort()
		for fmt in fmts:
			self.addRow(fmt, pg2)
		sz.setColExpand(1, True)

		sz = pg3.Sizer = dabo.ui.dSizer("V", DefaultBorder=10, DefaultBorderLeft=True,
		                                DefaultBorderRight=True)
		sz.appendSpacer(10)
		lbl = dabo.ui.dLabel(pg3, Caption="Check/Uncheck the following InputCodes to apply them\n" +
		                     "to the textbox below. Then type into the textbox to see\nthe effect that each code has.",
		                     FontBold=True, Alignment="Center")
		sz.append(lbl, "x")
		sz.appendSpacer(5)
		gsz = dabo.ui.dGridSizer(MaxCols=4, HGap=25, VGap=5)
		lbl = dabo.ui.dLabel(pg3, Caption="General Codes", FontBold=True)
		gsz.append(lbl, halign="center", colSpan=4)
		chk = dabo.ui.dCheckBox(pg3, Caption="_", ToolTipText="Allow Spaces",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		chk = dabo.ui.dCheckBox(pg3, Caption="R", ToolTipText="Right Align",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		chk = dabo.ui.dCheckBox(pg3, Caption="r", ToolTipText="Right Insert",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		chk = dabo.ui.dCheckBox(pg3, Caption="<", ToolTipText="Stay in field until explicit navigation",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		chk = dabo.ui.dCheckBox(pg3, Caption=">", ToolTipText="Insert/delete inside fields",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		chk = dabo.ui.dCheckBox(pg3, Caption="F", ToolTipText="Auto-fit field width",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		chk = dabo.ui.dCheckBox(pg3, Caption="V", ToolTipText="Validate against ValidRegex property",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		chk = dabo.ui.dCheckBox(pg3, Caption="S", ToolTipText="Select full field",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		sz.append(gsz, 1, halign="center")
		sz.appendSpacer(5)

		gsz = dabo.ui.dGridSizer(MaxCols=2, HGap=25, VGap=5)
		lbl = dabo.ui.dLabel(pg3, Caption="Character Codes", FontBold=True)
		gsz.append(lbl, halign="center", colSpan=2)
		chk = dabo.ui.dCheckBox(pg3, Caption="!", ToolTipText="Force Upper Case",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		chk = dabo.ui.dCheckBox(pg3, Caption="^", ToolTipText="Force Lower Case",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		txt = self.charText = dabo.ui.dMaskedTextBox(pg3, Value="", Mask="C{30}")
		gsz.append(txt, "x", colSpan=2)
		sz.append(gsz, 1, halign="center")
		sz.appendSpacer(5)

		gsz = dabo.ui.dGridSizer(MaxCols=2, HGap=25, VGap=5)
		lbl = dabo.ui.dLabel(pg3, Caption="Numeric Codes", FontBold=True)
		gsz.append(lbl, halign="center", colSpan=2)
		chk = dabo.ui.dCheckBox(pg3, Caption=",", ToolTipText="Allow grouping character in numeric values",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		chk = dabo.ui.dCheckBox(pg3, Caption="-", ToolTipText="Reserve space for leading sign for negatives",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		chk = dabo.ui.dCheckBox(pg3, Caption="0", ToolTipText="Leading Zeros in integer fields",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		gsz.appendSpacer(1)
		txt = self.numText = dabo.ui.dMaskedTextBox(pg3, Value="", Mask="#{30}")
		gsz.append(txt, "x", colSpan=2)
		sz.append(gsz, 1, halign="center")
		sz.appendSpacer(5)

		gsz = dabo.ui.dGridSizer(MaxCols=2, HGap=25, VGap=5)
		lbl = dabo.ui.dLabel(pg3, Caption="Date/DateTime/Time Codes", FontBold=True)
		gsz.append(lbl, halign="center", colSpan=2)
		chk = dabo.ui.dCheckBox(pg3, Caption="D", ToolTipText="Date/Datetime field",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		chk = dabo.ui.dCheckBox(pg3, Caption="T", ToolTipText="Time Field",
		                        OnHit=self.onCheckHit)
		gsz.append(chk)
		txt = self.dateText = dabo.ui.dMaskedTextBox(pg3, InputCodes="D", Value=datetime.date.today())
		gsz.append(txt, "x", colSpan=2)
		sz.append(gsz, 1, halign="center")

	def _lookup(self, evt):
		pass

	def onCheckHit(self, evt):
		chk = evt.EventObject
		cap = chk.Caption
		val = chk.Value
		print(cap, val)
		txts = (self.charText, self.numText, self.dateText)
		if cap in "!^":
			# Char
			txts = (self.charText, )
		elif cap in ",-0":
			# Num
			txts = (self.numText, )
		elif cap in "DT":
			# Num
			txts = (self.dateText, )
		for txt in txts:
			if val:
				txt.InputCodes += cap
			else:
				txt.InputCodes = txt.InputCodes.replace(chk.Caption, "")
			txt.setFocus()
			txt.refresh()

	def addRow(self, fmt, parent):
		sz = parent.Sizer
		sz.append(dabo.ui.dLabel(parent, Caption="%s:" % fmt), halign="right")
		sz.append(dMaskedTextBox(parent, Width=240, Format=fmt))


if __name__ == "__main__":
	import test
	test.Test().runTest(_dMaskedTextBox_test)
