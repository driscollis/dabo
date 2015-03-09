# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dListControl


class _dListControl_test(dListControl):
	def afterInit(self):
		self.setColumns(("Title", "Subtitle", "Release Year"))
		self.setColumnWidth(0, 150)
		self.setColumnWidth(1, 100)
		self.setColumnWidth(2, 200)
		self.append(("The Phantom Menace", "Episode 1", 1999))
		self.append(("Attack of the Clones", "Episode 2", 2002))
		self.append(("Revenge of the Sith", "Episode 3", 2005))
		self.append(("A New Hope", "Episode 4", 1977))
		self.append(("The Empire Strikes Back", "Episode 5", 1980))
		self.append(("Return of the Jedi", "Episode 6", 1983))

		self.Keys = [0, 1, 2, 3, 4, 5]

	def initProperties(self):
		self.MultipleSelect = True
		self.HorizontalRules = True
		self.VerticalRules = True
		#self.HeaderVisible = False

	def onHit(self, evt):
		print("KeyValue: ", self.KeyValue)
		print("PositionValue: ", self.PositionValue)
		print("StringValue: ", self.StringValue)
		print("Value: ", self.Value)

	def onListSelection(self, evt):
		print("List Selection!", self.Value, self.LastSelectedIndex, self.SelectedIndices)


	def onListDeselection(self, evt):
		print("Row deselected:", evt.EventData["index"])


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dListControl_test)
