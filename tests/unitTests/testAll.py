"""
Run all tests, using unittest discovery and coverage if installed.
"""

import os
import sys

import unittest
try:
	import coverage
except ImportError:
	coverage = None
import sys

if coverage:
	coverage.erase()
	coverage.start()

	coverage.exclude('if __name__ == "__main__":')

import dabo.ui
dabo.ui.loadUI('wx')

if __name__ == "__main__":
	tl = unittest.TestLoader()
	ts = tl.discover(start_dir=os.getcwd())
	unittest.TextTestRunner(verbosity=2).run(ts)

	if coverage:
		coverage.stop()
		#You can uncomment this to get test coverage on a particular module, but if you want to
		#see the entire report for dabo, run "python CoverageReport.py".  I would pipe it to a file though
		#coverage.report([dabo.dColors, dabo.dObject, dabo])
