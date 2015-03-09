# -*- coding: utf-8 -*-
from wx import glcanvas
import wx
import dabo
from . import controlmixin as cm
from dabo.dLocalize import _
from dabo.ui import makeDynamicProperty

try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	openGL = True
except ImportError:
	openGL = False
except Exception as e:
	# Report the error, and abandon the import
	dabo.log.error(_("Error importing OpenGL: %s") % e)
	openGL = False


class dGlWindow(cm.dControlMixin, glcanvas.GLCanvas):
	def __init__(self, parent, properties=None, attProperties=None, *args, **kwargs):
		if not openGL:
			raise ImportError("PyOpenGL is not present, so dGlWindow cannot instantiate.")

		self.init = False
		self._rotate = self._pan = False

		#set initial mouse position for rotate
		self.lastx = self.x = 30
		self.lasty = self.y = 30
		self._leftDown = self._rightDown = False

		self._baseClass = dGlWindow
		preClass = glcanvas.GLCanvas
		cm.dControlMixin.__init__(self, preClass, parent, properties=properties,
				attProperties=attProperties, *args, **kwargs)

	def initGL(self):
		"""Hook function.  Put your initial GL code in here."""
		pass


	def onDraw(self):
		"""
		Hook function.  Put the code here for what happens when you draw.

		.. note::
			You don't need to swap buffers here....We do this for you automatically.

		"""
		pass

	def afterInit(self):
		if dabo.ui.phoenix:
			self._context = glcanvas.GLContext(self)
			self._context.SetCurrent(self)
			self.SwapBuffers()


	def onResize(self, event):
		if not dabo.ui.phoenix:
			if self.GetContext():
				self.SetCurrent()

		glViewport(0, 0, self.Width, self.Height)


	def onPaint(self, event):
		dc = wx.PaintDC(self)
		if dabo.ui.phoenix:
			self.SetCurrent(self._context)
		else:
			self.SetCurrent()
		if not self.init:
			self.initGL()
			self.init = True
		self._onDraw()


	def _onDraw(self):
		#Call user hook method
		self.onDraw()

		if self.Rotate:
			glRotatef((self.y - self.lasty), 0.0, 0.0, 1.0);
			glRotatef((self.x - self.lastx), 1.0, 0.0, 0.0);

		#if self.Pan:
		#	pass

		self.SwapBuffers()


	def onMouseRightDown(self, evt):
		self.x, self.y = self.lastx, self.lasty = evt.EventData["mousePosition"]
		self._rightDown = True


	def onMouseRightUp(self, evt):
		self._rightDown = False

	#def onMouseLeftDown(self, evt):
		#pass

	#def onMouseLeftUp(self, evt):
		#pass

	def onMouseMove(self, evt):
		if self._rightDown:	#want to rotate object
			self.lastx, self.lasty = self.x, self.y	#store the previous x and y
			self.x, self.y = evt.EventData["mousePosition"]	#store the new x,y so we know how much to rotate
			self.Refresh(False)	#Mark window as "dirty" so it will be repainted

	# Getters and Setters
	def _getRotate(self):
		return self._rotate

	def _setRotate(self, val):
		self._rotate = val

	# Property Definitions
	Rotate = property(_getRotate, _setRotate, None,
		_("Rotate on Right Mouse Click and Drag"))
