# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dLinePlot

try:
	import numpy.oldnumeric as _Numeric
except ImportError:
	_Numeric = False
except Exception as e:
	# Report the error, and abandon the import
	dabo.log.error(_("Error importing numpy.oldnumeric: %s") % e)
	_Numeric = False

class _dLinePlot_test(dLinePlot):
	def initProperties(self):
		self.XAxisLabel = "X Axis"
		self.YAxisLabel = "Y Axis"
		self.Caption = "Title of Graph"


	def afterInit(self):
		# 1000 points cos function, plotted as blue line
		self.appendLineFromEquation("2*_Numeric.cos(%s)", 5, 10, Caption="Blue Line", LineWidth=2, LineColor="blue")

		line = []
		for i in range(10):
			line.append((i, float(i)/2))
		self.appendLineFromPoints(line)

		data1 = 2.*_Numeric.pi*_Numeric.arange(200)/200.
		data1.shape = (100, 2)
		data1[:, 1] = _Numeric.sin(data1[:, 0])
		self.appendMarkerFromPoints(data1, Caption='Green Markers', Color='green', MarkerShape='circle', MarkerSize=1)

		# A few more points...
		points = [(0., 0.), (_Numeric.pi/4., 1.), (_Numeric.pi/2, 0.), (3.*_Numeric.pi/4., -1)]
		self.appendMarkerFromPoints(points, Caption='Cross Legend', Color='blue', MarkerShape='cross')


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dLinePlot_test)
