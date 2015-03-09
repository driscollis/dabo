#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")

from dabo.ui import dForm
from dabo.ui import dImage


class _dImage_test(dabo.ui.dForm):
	def afterInit(self):
		self.Caption = "dImage Demonstration"
		self.mainPanel = mp = dabo.ui.dPanel(self)
		self.Sizer.append1x(mp)
		sz = dabo.ui.dSizer("v")
		mp.Sizer = sz
		# Create a panel with horiz. and vert.  sliders
		self.imgPanel = dabo.ui.dPanel(mp)
		self.VSlider = dabo.ui.dSlider(mp, Orientation="V", Min=1, Max=100,
	        Value=100, OnHit=self.onSlider)
		self.HSlider = dabo.ui.dSlider(mp, Orientation="H", Min=1, Max=100,
	        Value=100, OnHit=self.onSlider)

		psz = self.imgPanel.Sizer = dabo.ui.dSizer("V")
		hsz = dabo.ui.dSizer("H")
		hsz.append1x(self.imgPanel)
		hsz.appendSpacer(10)
		hsz.append(self.VSlider, 0, "x")
		sz.DefaultBorder = 25
		sz.DefaultBorderLeft = sz.DefaultBorderRight = True
		sz.appendSpacer(25)
		sz.append(hsz, 1, "x")
		sz.appendSpacer(10)
		sz.append(self.HSlider, 0, "x")
		sz.appendSpacer(10)

		# Create the image control
		self.img = dImage(self.imgPanel)

		hsz = dabo.ui.dSizer("H")
		hsz.DefaultSpacing = 10
		dabo.ui.dBitmapButton(mp, RegID="btnRotateCW", Picture="rotateCW",
	            OnHit=self.onRotateCW, Size=(36, 36))
		dabo.ui.dBitmapButton(mp, RegID="btnRotateCCW", Picture="rotateCCW",
	            OnHit=self.onRotateCCW, Size=(36, 36))
		dabo.ui.dBitmapButton(mp, RegID="btnFlipHorizontal", Picture="flip_horiz",
	            OnHit=self.onFlipHoriz, Size=(36, 36))
		dabo.ui.dBitmapButton(mp, RegID="btnFlipVertical", Picture="flip_vert",
	            OnHit=self.onFlipVert, Size=(36, 36))
		hsz.append(self.btnRotateCW)
		hsz.append(self.btnRotateCCW)
		hsz.append(self.btnFlipHorizontal)
		hsz.append(self.btnFlipVertical)

		self.ddScale = dabo.ui.dDropdownList(mp,
	            Choices=["Proportional", "Stretch", "Clip"],
	            DataSource="self.Form.img",
	            DataField="ScaleMode")
		self.ddScale.PositionValue = 0
		btn = dabo.ui.dButton(mp, Caption="Load Image",
	            OnHit=self.onLoadImage)
		btnOK = dabo.ui.dButton(mp, Caption="Done", OnHit=self.close)
		hsz.append(self.ddScale, 0, "x")
		hsz.append(btn, 0, "x")
		hsz.append(btnOK, 0, "x")
		sz.append(hsz, 0, alignment="right")
		sz.appendSpacer(25)

		# Set the idle update flage
		self.needUpdate = False


	def onRotateCW(self, evt):
		self.img.rotateClockwise()


	def onRotateCCW(self, evt):
		self.img.rotateCounterClockwise()


	def onFlipVert(self, evt):
		self.img.flipVertically()

	def onFlipHoriz(self, evt):
		self.img.flipHorizontally()


	def onSlider(self, evt):
		# Vertical sliders have their low value on the bottom on OSX;
		# on MSW and GTK, the low value is at the top
		val = evt.EventObject.Value * 0.01
		dir = evt.EventObject.Orientation[0].lower()
		if dir == "h":
			# Change the width of the image
			self.img.Width = (self.imgPanel.Width * val)
		else:
			self.img.Height = (self.imgPanel.Height * val)


	def onLoadImage(self, evt):
		f = dabo.ui.getFile("jpg", "png", "gif", "bmp", "tif", "ico", "*")
		if f:
			self.img.Picture = f


	def onResize(self, evt):
		self.needUpdate = True


	def onIdle(self, evt):
		if self.needUpdate:
			self.needUpdate = False
			wd = self.HSlider.Value * 0.01 * self.imgPanel.Width
			ht = self.VSlider.Value * 0.01 * self.imgPanel.Height
			self.img.Size = (wd, ht)


if __name__ == "__main__":
	from dabo.dApp import dApp
	app = dApp()
	app.MainFormClass = _dImage_test
	app.start()

