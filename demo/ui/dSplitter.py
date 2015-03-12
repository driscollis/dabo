# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dSplitter

from dabo import dColors

import random


class _dSplitter_test(dSplitter):
	def __init__(self, *args, **kwargs):
		kwargs["createPanes"] = True
		super(_dSplitter_test, self).__init__(*args, **kwargs)

	def initProperties(self):
		self.Width = 250
		self.Height = 200
		self.MinimumPanelSize = 20
		self.ShowPanelSplitMenu = True

	def afterInit(self):
		self.Panel1.BackColor = random.choice(list(dColors.colorDict.values()))
		self.Panel2.BackColor = random.choice(list(dColors.colorDict.values()))


	def onSashDoubleClick(self, evt):
		if not dabo.ui.areYouSure("Remove the sash?", cancelButton=False):
			evt.stop()


if __name__ == "__main__":
	import test
	test.Test().runTest(_dSplitter_test)
