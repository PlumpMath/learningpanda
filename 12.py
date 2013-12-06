from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from random import randint

import math

class Enemy:
	def __init__(self, model):
		self.enemy = model
		self.enemy.setScale(1, 1, 1)
		self.enemy.reparentTo(app.render)
		self.x = randint(-100, 100)
		self.y = randint(70, 200)
		self.s = 1

	def update(self):

		endx = app.player.x
		endy = app.player.y
		angle = math.atan2((endy - self.y), (endx - self.x))
		dx = self.s * math.cos(angle)
		dy = self.s * math.sin(angle)
		self.y = self.y + dy
		self.x = self.x + dx
		self.enemy.setPos(self.x, self.y, 0)

class Player:
	def __init__(self, actor):
		self.actor = actor
		self.x = 0
		self.y = 0
		self.z = 0
		self.h = -180
		self.p = 0
		self.r = 0
		self.s = 1 # speed
		self.dir = "stop"

		self.actor.setScale(0.005, 0.005, 0.005)

	def update(self):
		if self.dir == "up":
			self.y = self.y  + self.s
		elif self.dir == "down":
			self.y  = self.y  - self.s
		elif self.dir == "left":
			self.x = self.x - self.s
		elif self.dir == "right":
			self.x = self.x + self.s

		self.actor.setPos(self.x, self.y, self.z)
		self.actor.setHpr(self.h, self.p, self.r)

class Bullet:
	def __init__(self, dir, model, x, y):
		self.bullet = model
		self.x = x
		self.y = y
		self.dir = dir
		self.s = 2 # speed

		self.bullet.setScale(1, 1, 1,)
		self.bullet.reparentTo(app.render)

	def update(self):
		if self.dir == "up":
			self.y = self.y + self.s
		elif self.dir == "down":
			self.y = self.y - self.s
		elif self.dir == "left":
			self.x = self.x - self.s
		elif self.dir == "right":
			self.x = self.x + self.s

		self.bullet.setPos(self.x, self.y, 0)

		for x in app.enemies:
			dis = app.distance(self.x, x.x, self.y, x.y)
			if dis < 2:
				try:
				    app.enemies.remove(x)
				except ValueError:
				    pass
				try:
				    app.bullets.remove(self)
				except ValueError:
				    pass

class App(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		self.disableMouse()

		self.enemies = []
		self.bullets = []
		self.counter = 0

		self.camera_d = {
			"x": 0,
			"y": 0,
			"z": 50,
			"h": 0,
			"p": -90,
			"r": 0
		}

		# prepare terrain
		self.env = self.loader.loadModel("models/environment")
		self.env.setScale(0.25, 0.25, 0.25)
		self.env.setPos(-8, 42, 0)
		self.env.reparentTo(self.render)

		# player
		self.player = Player(Actor("models/panda-model", {"walk": "models/panda-walk4"}))

		# tasks
		self.taskMgr.add(self.update, "update")

		# controls
		self.accept("w", self.move, ["up"])
		self.accept("s", self.move, ["down"])
		self.accept("a", self.move, ["left"])
		self.accept("d", self.move, ["right"])
		self.accept("w-up", self.stop_move)
		self.accept("s-up", self.stop_move)
		self.accept("a-up", self.stop_move)
		self.accept("d-up", self.stop_move)

		self.accept("arrow_up", self.shoot, ["up"])
		self.accept("arrow_down", self.shoot, ["down"])
		self.accept("arrow_left", self.shoot, ["left"])
		self.accept("arrow_right", self.shoot, ["right"])

	def move(self, dir):
		self.player.dir = dir
		self.player.actor.loop("walk")

	def stop_move(self):
		self.player.dir = "stop"
		self.player.actor.stop()

	def distance(self, x1,x2,y1,y2):
	    sq1 = (x1-x2)*(x1-x2)
	    sq2 = (y1-y2)*(y1-y2)
	    return math.sqrt(sq1 + sq2)

	def shoot(self, dir):
		bullet = Bullet(dir, self.loader.loadModel("models/box"), 
						self.player.x, self.player.y)
		self.bullets.append(bullet)

	def enemy(self):
		enemy = Enemy(loader.loadModel("models/teapot"))
		self.enemies.append(enemy)

	def update(self, task):
		# print len(self.bullets)

		self.counter = self.counter + 1

		if self.counter == 40:
			self.enemy()
			self.counter = 0

		self.player.update()

		self.camera.setPos(self.player.x, self.player.y,
						   self.camera_d["z"])
		self.camera.setHpr(self.camera_d["x"], self.camera_d["p"],
						   self.camera_d["r"])

		for v in self.bullets:
			v.update()

		for v in self.enemies:
			v.update()

		return Task.cont

	def __del__(self):
		self.taskMgr.remove(self.update)

app = App()
app.player.actor.reparentTo(app.render)
app.run()