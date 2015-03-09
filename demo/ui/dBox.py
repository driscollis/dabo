# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dBox


class _dBox_test(dBox):
	def __init__(self, parent, label='a test', *args, **kwargs):
		super(_dBox_test, self).__init__(parent, label='the dBox label', *args, **kwargs)
		
	def initProperties(self):
		self.Width = 100
		self.Height = 20


if __name__ == "__main__":
	import test
	test.Test().runTest(_dBox_test)
