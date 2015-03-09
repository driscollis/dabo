# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dHtmlBox
from dabo.ui import dEvents

import datetime


class _dHtmlBox_test(dHtmlBox):
	def initProperties(self):
		self.BorderWidth = 5
		self.BorderColor = "darkblue"
		self.OpenLinksInBrowser = True
		self.Source = self.getPageData()

	def getPageData(self):
		return """<html>
		<body bgcolor="#B0C4DE">
		<center>
			<table bgcolor="#8470FF" width="100%%" cellspacing="0" cellpadding="0"
					border="1">
				<tr>
					<td align="center"><h1>dHtmlBox</h1></td>
				</tr>
			</table>
		</center>
		<p><b><font size="+2" color="#FFFFFF">dHtmlBox</font></b> is a Dabo UI widget that is designed to display html text.
		Be careful, though, because the widget doesn't support advanced functions like
		Javascript parsing.</p>
		<p>It's better to think of it as a way to display <b>rich text</b> using
		<font size="+1" color="#993300">HTML markup</font>, rather
		than a web browser replacement, although you <i>can</i> create links that will open
		in a web browser, like this: <a href="http://wiki.dabodev.com">Dabo Wiki</a>.</p>

		<p>&nbsp;</p>
		<div align="center"><img src="daboIcon.ico"></div>

		<p align="center"><b><a href="http://dabodev.com">Dabo</a></b> is brought to you by <b>Ed Leafe</b>, <b>Paul McNett</b>,
		and others in the open source community. Copyright &copy; 2004-%s
		</p>
		</body>
		</html>
		""" % datetime.date.today().year

	def onMouseLeftDown(self, evt):
		print("mousedown")
		self.SetFocusIgnoringChildren()

	def onKeyDown(self, evt):
		print("Key Code:", evt.EventData["keyCode"])


def textChangeHandler(evt):
	dabo.ui.callAfter(evt.EventObject.flushValue)

def resetHTML(evt):
	frm = evt.EventObject.Form
	frm.htmlbox.Source = frm.htmlbox.getPageData()
	frm.update()



if __name__ == "__main__":
	from dabo.dApp import dApp
	app = dApp(MainFormClass=None)
	app.setup()
	frm = dabo.ui.dForm()
	pnl = dabo.ui.dPanel(frm)
	frm.Sizer.append1x(pnl)
	sz = pnl.Sizer = dabo.ui.dSizer("v")
	ht = _dHtmlBox_test(pnl, RegID="htmlbox")
	sz.append(ht, 2, "x", border=10)
	lbl = dabo.ui.dLabel(pnl, Caption="Edit the HTML below, then press 'Tab' to update the rendered HTML")
	sz.appendSpacer(5)
	sz.append(lbl, halign="center")
	edt = dabo.ui.dEditBox(pnl, RegID="editbox", DataSource=ht, DataField="Source")
	edt.bindEvent(dEvents.KeyChar, textChangeHandler)
	sz.append1x(edt, border=10)
	btn = dabo.ui.dButton(pnl, Caption="Reset", OnHit=resetHTML)
	sz.append(btn, halign="right", border=10, borderSides=["right", "bottom"])

	frm.show()
	app.start()
