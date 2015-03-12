# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dForm
from dabo.ui import dTreeView
from dabo.ui import dNode

from dabo import dEvents
from dabo.dLocalize import _


class TestNode(dNode):
	def afterInit(self):
		self.ForeColor = "darkred"
		self.FontItalic = True
		self.FontSize += 3


class _dTreeView_test(dTreeView):
	def afterInit(self):
		self.NodeClass = TestNode
		self.addDummyData()
		self.expandAll()
		self.Hover = True
		self.ToolTipText = _("Default ToolTip for the Tree")
		self.ImageSize = (16, 16)

	def onHit(self, evt):
		print("Hit!")

	def onContextMenu(self, evt):
		print("Context menu on tree")

	def onMouseRightClick(self, evt):
		print("Mouse Right Click on tree")

	def onTreeSelection(self, evt):
		print("Selected node caption:", evt.EventData["selectedCaption"])

	def onTreeItemCollapse(self, evt):
		print("Collapsed node caption:", evt.EventData["selectedCaption"])

	def onTreeItemExpand(self, evt):
		print("Expanded node caption:", evt.EventData["selectedCaption"])

	def onTreeItemContextMenu(self, evt):
		itm = evt.itemID
		node = self.find(itm)[0]
		print("Context menu on item:", node.Caption)

	def onTreeBeginDrag(self, evt):
		print("Beginning drag for %s" % evt.selectedCaption)

	def onTreeEndDrag(self, evt):
		print("Ending drag for %s" % evt.selectedCaption)


class TreeViewTestForm(dForm):
	def afterInit(self):
		mp = dabo.ui.dPanel(self)
		self.Sizer.append1x(mp)
		sz = mp.Sizer = dabo.ui.dSizer("v")
		tree = self.tree = _dTreeView_test(mp)
		sz.append1x(tree, border=12)
		sz.DefaultBorder = 7
		sz.DefaultBorderLeft = sz.DefaultBorderTop = True

		chk = dabo.ui.dCheckBox(mp, Caption="Editable",
	            DataSource=tree, DataField="Editable")
		sz.append(chk, halign="Left")

		chk = dabo.ui.dCheckBox(mp, Caption="MultipleSelect",
	            DataSource=tree, DataField="MultipleSelect")
		sz.append(chk, halign="Left")

		chk = dabo.ui.dCheckBox(mp, Caption="ShowButtons",
	            DataSource=tree, DataField="ShowButtons")
		sz.append(chk, halign="Left")

		chk = dabo.ui.dCheckBox(mp, Caption="ShowLines",
	            DataSource=tree, DataField="ShowLines")
		sz.append(chk, halign="Left")

		chk = dabo.ui.dCheckBox(mp, Caption="ShowRootNode",
	            DataSource=tree, DataField="ShowRootNode")
		sz.append(chk, halign="Left")

		chk = dabo.ui.dCheckBox(mp, Caption="ShowRootNodeLines",
	            DataSource=tree, DataField="ShowRootNodeLines")
		sz.append(chk, halign="Left")

		chk = dabo.ui.dCheckBox(mp, Caption="UseNodeToolTips",
	            DataSource=tree, DataField="UseNodeToolTips")
		sz.append(chk, halign="Left")

		self.update()

		btnEx = dabo.ui.dButton(mp, Caption="Expand All")
		btnEx.bindEvent(dEvents.Hit, self.onExpandAll)
		btnCl = dabo.ui.dButton(mp, Caption="Collapse All")
		btnCl.bindEvent(dEvents.Hit, self.onCollapseAll)
		hsz = dabo.ui.dSizer("H")
		hsz.append(btnEx)
		hsz.appendSpacer(5)
		hsz.append(btnCl)
		sz.append(hsz)
		sz.appendSpacer(10)

	def onExpandAll(self, evt):
		self.tree.expandAll()

	def onCollapseAll(self, evt):
		self.tree.collapseAll()


if __name__ == "__main__":
	import test
	test.Test().runTest(TreeViewTestForm)
