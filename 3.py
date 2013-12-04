from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		# load the environment model
		self.env = self.loader.loadModel("models/environment")
		self.env.reparentTo(self.render)

		# apply scale and position transforms on the model
		self.env.setScale(0.25, 0.25, 0.25)
		self.env.setPos(-8, 42, 0)

app = MyApp()
app.run()