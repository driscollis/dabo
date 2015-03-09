# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dEditBox


class _dEditBox_test(dEditBox):
	def initProperties(self):
		self.Value = """Love, exciting and new
Come aboard, we're expecting you
Love, life's sweetest reward
Let it flow, it floats back to you

Love Boat soon will be making another run
The Love Boat promises something for everyone
Set a course for adventure
Your mind on a new romance

Love won't hurt anymore
It's an open smile on a friendly shore
Yes love...
It's love...

Love Boat soon will be making another run
The Love Boat promises something for everyone
Set a course for adventure
Your mind on a new romance

Love won't hurt anymore
It's an open smile on a friendly shore
It's love...
It's love...
It's love...
It's the Love Boat
It's the Love Boat
"""
	def afterInit(self):
		self.Form.Size = (444, 244)
		dabo.ui.callAfter(self.adjustFormCaption)
	def adjustFormCaption(self):
		newcap = "%s - WordWrap: %s" % (self.Form.Caption, self.WordWrap)
		self.Form.Caption = newcap


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dEditBox_test, WordWrap=True)
	test.Test().runTest(_dEditBox_test, WordWrap=False)
