# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dDockForm


class _dDockForm_test(dDockForm):
	def initProperties(self):
		self.SaveRestorePosition = False
		self.Size = (700, 500)

	def afterInit(self):
		self.fp = self.addPanel(Floating=True, BackColor="orange",
				Caption="Initially Floating", Top=70, Left=200, Size=(144, 100))
		self.dp = self.addPanel(Floating=False, Caption="Initially Docked", BackColor="slateblue",
				ShowCaption=False, ShowPinButton=True, ShowCloseButton=False,
				ShowGripper=True, Size=(144, 100))
		btn = dabo.ui.dButton(self.CenterPanel, Caption="Test Orange", OnHit=self.onTestFP)
		self.CenterPanel.Sizer.append(btn)
		btn = dabo.ui.dButton(self.CenterPanel, Caption="Test Blue", OnHit=self.onTestDP)
		self.CenterPanel.Sizer.append(btn)
		chk = dabo.ui.dCheckBox(self.CenterPanel, Caption="Orange Dockable", DataSource=self.fp,
				DataField="Dockable")
		self.CenterPanel.Sizer.append(chk)
		self.fp.DynamicCaption = self.capForOrange

	def capForOrange(self):
		print("ORNG CAP", self.fp.Docked)
		state = "Floating"
		if self.fp.Docked:
			state = "Docked"
		print("STATE", state)
		return "I'm %s!" % state

	def onTestFP(self, evt):
		self.printTest(self.fp)
	def onTestDP(self, evt):
		self.printTest(self.dp)
	def printTest(self, obj):
		nm = {self.fp: "OrangePanel", self.dp: "BluePanel"}[obj]
		print(nm + ".BottomDockable:", obj.BottomDockable)
		print(nm + ".Caption:", obj.Caption)
		print(nm + ".DestroyOnClose:", obj.DestroyOnClose)
		print(nm + ".Dockable:", obj.Dockable)
		print(nm + ".Docked:", obj.Docked)
		print(nm + ".Floatable:", obj.Floatable)
		print(nm + ".Floating:", obj.Floating)
		print(nm + ".FloatingBottom:", obj.FloatingBottom)
		print(nm + ".FloatingHeight:", obj.FloatingHeight)
		print(nm + ".FloatingLeft:", obj.FloatingLeft)
		print(nm + ".FloatingPosition:", obj.FloatingPosition)
		print(nm + ".FloatingRight:", obj.FloatingRight)
		print(nm + ".FloatingSize:", obj.FloatingSize)
		print(nm + ".FloatingTop:", obj.FloatingTop)
		print(nm + ".FloatingWidth:", obj.FloatingWidth)
		print(nm + ".GripperPosition:", obj.GripperPosition)
		print(nm + ".LeftDockable:", obj.LeftDockable)
		print(nm + ".Movable:", obj.Movable)
		print(nm + ".Resizable:", obj.Resizable)
		print(nm + ".RightDockable:", obj.RightDockable)
		print(nm + ".ShowBorder:", obj.ShowBorder)
		print(nm + ".ShowCaption:", obj.ShowCaption)
		print(nm + ".ShowCloseButton:", obj.ShowCloseButton)
		print(nm + ".ShowGripper:", obj.ShowGripper)
		print(nm + ".ShowMaximizeButton:", obj.ShowMaximizeButton)
		print(nm + ".ShowMinimizeButton:", obj.ShowMinimizeButton)
		print(nm + ".ShowPinButton:", obj.ShowPinButton)
		print(nm + ".TopDockable:", obj.TopDockable)
		print(nm + ".Visible:", obj.Visible)



if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dDockForm_test)
