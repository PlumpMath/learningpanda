from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task 

class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		# load environment
		self.env = self.loader.loadModel("models/environment")
		self.env.reparentTo(self.render)

		self.env.setScale(0.25, 0.25, 0.25)
		self.env.setPos(-8, 42, 0)

		self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

	def spinCameraTask(self, task):
		angleDegrees = task.time * 6.0
		angleRadians = angleDegrees * (pi / 180.0)
		self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
		self.camera.setHpr(angleDegrees, 0, 0)
		return Task.cont

app = MyApp()
app.run()