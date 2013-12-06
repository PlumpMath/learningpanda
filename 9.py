from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain

class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		terrain = GeoMipTerrain("worldTerrain")
		terrain.setHeightfield("models/issue1terrain.png")
		terrain.setColorMap("models/issue2terrain.png")
		terrain.setBruteforce(True) # level of detail
		root = terrain.getRoot()
		root.reparentTo(render)
		root.setSz(60) # maximum height
		terrain.generate()

		root.writeBamFile("models/world.bam")

app = MyApp()
app.run()