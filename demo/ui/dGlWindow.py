# -*- coding: utf-8 -*-
import dabo.ui
if __name__ == "__main__":
	dabo.ui.loadUI("wx")
	if __package__ is None:
		import dabo.ui.uiwx
		__package__ = "dabo.ui.uiwx"

from dabo.ui import dGlWindow


class _dGlWindow_test(dGlWindow):
	def initProperties(self):
		self.Rotate = True

	def initGL(self):
		# set viewing projection
		glMatrixMode(GL_PROJECTION)
		glFrustum(-0.5, 0.5, -0.5, 0.5, 1.0, 3.0)

		# position viewer
		glMatrixMode(GL_MODELVIEW)
		glTranslatef(0.0, 0.0, -2.0)

		# position object
		glRotatef(self.y, 1.0, 0.0, 0.0)
		glRotatef(self.x, 0.0, 1.0, 0.0)

		glEnable(GL_DEPTH_TEST)
		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)


	def onDraw(self):
		# clear color and depth buffers
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		# draw six faces of a cube
		glBegin(GL_QUADS)
		glNormal3f( 0.0, 0.0, 1.0)
		glVertex3f( 0.5, 0.5, 0.5)
		glVertex3f(-0.5, 0.5, 0.5)
		glVertex3f(-0.5, -0.5, 0.5)
		glVertex3f( 0.5, -0.5, 0.5)

		glNormal3f( 0.0, 0.0, -1.0)
		glVertex3f(-0.5, -0.5, -0.5)
		glVertex3f(-0.5, 0.5, -0.5)
		glVertex3f( 0.5, 0.5, -0.5)
		glVertex3f( 0.5, -0.5, -0.5)

		glNormal3f( 0.0, 1.0, 0.0)
		glVertex3f( 0.5, 0.5, 0.5)
		glVertex3f( 0.5, 0.5, -0.5)
		glVertex3f(-0.5, 0.5, -0.5)
		glVertex3f(-0.5, 0.5, 0.5)

		glNormal3f( 0.0, -1.0, 0.0)
		glVertex3f(-0.5, -0.5, -0.5)
		glVertex3f( 0.5, -0.5, -0.5)
		glVertex3f( 0.5, -0.5, 0.5)
		glVertex3f(-0.5, -0.5, 0.5)

		glNormal3f( 1.0, 0.0, 0.0)
		glVertex3f( 0.5, 0.5, 0.5)
		glVertex3f( 0.5, -0.5, 0.5)
		glVertex3f( 0.5, -0.5, -0.5)
		glVertex3f( 0.5, 0.5, -0.5)

		glNormal3f(-1.0, 0.0, 0.0)
		glVertex3f(-0.5, -0.5, -0.5)
		glVertex3f(-0.5, -0.5, 0.5)
		glVertex3f(-0.5, 0.5, 0.5)
		glVertex3f(-0.5, 0.5, -0.5)
		glEnd()


class _dGlWindow_test2(dGlWindow):
	def initProperties(self):
		self.Rotate = True

	def initGL(self):
		glMatrixMode(GL_PROJECTION)
		# camera frustrum setup
		glFrustum(-0.5, 0.5, -0.5, 0.5, 1.0, 3.0)
		glMaterial(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
		glMaterial(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
		glMaterial(GL_FRONT, GL_SPECULAR, [1.0, 0.0, 1.0, 1.0])
		glMaterial(GL_FRONT, GL_SHININESS, 50.0)
		glLight(GL_LIGHT0, GL_AMBIENT, [0.0, 1.0, 0.0, 1.0])
		glLight(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
		glLight(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
		glLight(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
		glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)
		glDepthFunc(GL_LESS)
		glEnable(GL_DEPTH_TEST)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		# position viewer
		glMatrixMode(GL_MODELVIEW)
		# position viewer
		glTranslatef(0.0, 0.0, -2.0);
		#
		glutInit([])

	def onDraw(self):
		# clear color and depth buffers
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		# use a fresh transformation matrix
		glPushMatrix()
		# position object
		#glTranslate(0.0, 0.0, -2.0)
		glRotate(30.0, 1.0, 0.0, 0.0)
		glRotate(30.0, 0.0, 1.0, 0.0)

		glTranslate(0, -1, 0)
		glRotate(250, 1, 0, 0)
		glutSolidCone(0.5, 1, 30, 5)
		glPopMatrix()


if __name__ == "__main__":
	from . import test
	test.Test().runTest(_dGlWindow_test)
	test.Test().runTest(_dGlWindow_test2)
