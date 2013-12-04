import direct.directbase.DirectStart
from panda3d.core import AmbientLight, DirectionalLight, LightAttrib
from panda3d.core import NodePath
from panda3d.core import Vec3, Vec4
from direct.interval.IntervalGlobal import * # needed for intervals
from direct.gui.DirectGui import *

# import path constants and functions
from math import pi, sin

class World:
	def __init__(self):
		# on screen title
		self.title = OnscreenText(text="Panda3d: Tutorial 2 - Carousel",
								  style=1, fg=(1, 1, 1, 1),
								  pos=(0.87, -0.95), scale=.07)

		base.setBackgroundColor(.6, .6, 1)
		# base.disableMouse()
		camera.setPosHpr(0, -8, 2.5, 0, -9, 0) # set cameras position and orientation

		self.loadModels()
		self.setupLights()
		self.startCarousel()

	def loadModels(self):
		# load carousel base
		self.carousel = loader.loadModel("models/carousel_base")
		self.carousel.reparentTo(render) # attach it to render

		self.lights1 = loader.loadModel("models/carousel_lights")
		self.lights1.reparentTo(self.carousel)

		self.lights2 = loader.loadModel("models/carousel_lights")
		self.lights2.setH(36)
		self.lights2.reparentTo(self.carousel)

		self.lightOffTex = loader.loadTexture("models/carousel_lights_off.jpg")
		self.lightOnTex = loader.loadTexture("models/carousel_lights_on.jpg")

		self.pandas = [self.carousel.attachNewNode("panda" + str(i))
					   for i in range(4)]
		self.models = [loader.loadModel("models/carousel_panda")
					   for i in range(4)]
		self.moves = [0 for i in range(4)]

		for i in range(4):
			self.pandas[i].setPosHpr(0, 0, 1.3, i*90, 0, 0)

			self.models[i].reparentTo(self.pandas[i])
			self.models[i].setY(.85)

		self.env = loader.loadModel("models/env")
		self.env.reparentTo(render)
		self.env.setScale(7)

	def setupLights(self):
		ambientLight = AmbientLight("ambientLight")
		ambientLight.setColor(Vec4(.4, .4, .35, 1))
		directionalLight = DirectionalLight("directionalLight")
		directionalLight.setDirection(Vec3(0, 8, -2.5))
		directionalLight.setColor(Vec4(0.9, 0.8, 0.9, 1))
		render.setLight(render.attachNewNode(directionalLight))
		render.setLight(render.attachNewNode(directionalLight))

		self.env.setLightOff()

	def startCarousel(self):
		self.carouselSpin = self.carousel.hprInterval(20, Vec3(360, 0, 0))
		self.carouselSpin.loop()

		for i in range(4):
			self.moves[i] = LerpFunc(
					self.oscilatePanda,
					duration = 3,
					fromData = 0,
					toData = 2 * pi,
					extraArgs = [self.models[i], pi*(i%2)]
				)

			self.moves[i].loop()


		self.lightBlink = Sequence(
				Parallel(
					Func(self.lights1.setTexture, self.lightOnTex, 1),
					Func(self.lights2.setTexture, self.lightOffTex, 1)),

				Wait(1),

				Parallel(
					Func(self.lights1.setTexture, self.lightOffTex, 1),
					Func(self.lights2.setTexture, self.lightOnTex, 1)),

				Wait(1)
			)

		self.lightBlink.loop()

	def oscilatePanda(self, rad, panda, offset):
		panda.setZ(sin(rad + offset) * .2)

w = World()

run()