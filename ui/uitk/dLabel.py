import Tkinter, dabo, dabo.ui

if __name__ == "__main__":
	dabo.ui.loadUI("tk")

import dControlMixin as cm

class dLabel(Tkinter.Label, cm.dControlMixin):
	""" Create a static (not data-aware) label.
	"""
	def __init__(self, master, cnf={}, name='dLabel', *args, **kwargs):

		self._baseClass = dLabel

		self._beforeInit()

		Tkinter.Label.__init__(self, master, cnf, name=name, *args, **kwargs)

		cm.dControlMixin.__init__(self, name)
		self._afterInit()

		self.pack()
		

	def initEvents(self):
		dLabel.doDefault()


# 	# property get/set functions
# 	def _getAutoResize(self):
# 		return not self.hasWindowStyleFlag(wx.ST_NO_AUTORESIZE)
# 	def _setAutoResize(self, value):
# 		self.delWindowStyleFlag(wx.ST_NO_AUTORESIZE)
# 		if not value:
# 			self.addWindowStyleFlag(wx.ST_NO_AUTORESIZE)
# 
# 	def _getAlignment(self):
# 		if self.hasWindowStyleFlag(wx.ALIGN_RIGHT):
# 			return 'Right'
# 		elif self.hasWindowStyleFlag(wx.ALIGN_CENTRE):
# 			return 'Center'
# 		else:
# 			return 'Left'
# 
# 	def _getAlignmentEditorInfo(self):
# 		return {'editor': 'list', 'values': ['Left', 'Center', 'Right']}
# 
# 	def _setAlignment(self, value):
# 		# Note: Alignment must be set before object created.
# 		self.delWindowStyleFlag(wx.ALIGN_LEFT)
# 		self.delWindowStyleFlag(wx.ALIGN_CENTRE)
# 		self.delWindowStyleFlag(wx.ALIGN_RIGHT)
# 
# 		value = str(value)
# 
# 		if value == 'Left':
# 			self.addWindowStyleFlag(wx.ALIGN_LEFT)
# 		elif value == 'Center':
# 			self.addWindowStyleFlag(wx.ALIGN_CENTRE)
# 		elif value == 'Right':
# 			self.addWindowStyleFlag(wx.ALIGN_RIGHT)
# 		else:
# 			raise ValueError, ("The only possible values are "
# 							"'Left', 'Center', and 'Right'.")
# 
# 	# property definitions follow:
# 	AutoResize = property(_getAutoResize, _setAutoResize, None,
# 		'Specifies whether the length of the caption determines the size of the label. (bool)')
# 	Alignment = property(_getAlignment, _setAlignment, None,
# 						'Specifies the alignment of the text. (str) \n'
# 						'   Left (default) \n'
# 						'   Center \n'
# 						'   Right')

if __name__ == "__main__":
	import test
	test.Test().runTest(dLabel)
