from pyglet import *
from pyglet.sprite import *
from pyglet.window import *
import pyglet
import random

import ente




class SpaceGameWindow(window.Window):
	batch = pyglet.graphics.Batch()
	
	screen_width = 600
	screen_height = 500
	
	tile_width = 60
	tile_height = 40
	
	#init the camera to the middle of the board, not important
	camera_x = -13*tile_width
	camera_y = 6*tile_height
	scroll_speed = 10
	
	terrain = []

	def __init__(self, keys, *args, **kwargs):
		self.keys = keys
		#Let all of the standard stuff pass through
		window.Window.__init__(self, width=self.screen_width,
			height=self.screen_height, *args, **kwargs)
		self.init_objects()

	def init_objects(self):
							
		self.stupid()
		
#		self.puddle = ente.Ente(puddle_image, 30*5+20, 10*5+5, 5, 5,
#			batch=self.batch, group=graphics.OrderedGroup(-5*2+1))


	def draw(self):
		self.batch.draw()

	def main_loop(self):
		while not self.has_exit:
			self.dispatch_events()
			self.clear()

			#Tick the clock
			clock.tick()
			
			self.check_keys()
				
			#Gets fps and draw it
			self.set_caption("fps: "+str(round(clock.get_fps())))
				
			self.draw()

			#update the screen
			self.flip()

	def check_keys(self):
		if self.keys[key.RIGHT]:
			space.camera_x = space.camera_x - 1*self.scroll_speed
			space.update_camera()	
		elif self.keys[key.LEFT]:
			space.camera_x = space.camera_x + 1*self.scroll_speed
			space.update_camera()	
		elif self.keys[key.DOWN]:
			space.camera_y = space.camera_y + 1*self.scroll_speed
			space.update_camera()	
		elif self.keys[key.UP]:
			space.camera_y = space.camera_y - 1*self.scroll_speed
			space.update_camera()
		elif self.keys[key.RETURN]:
			self.stupid()
		
	def update_camera(self):
		for object in self.terrain:
				object.update_camera(self.camera_x, self.camera_y, 
					self.tile_width, self.tile_height)
		
	def stupid(self):	
		room_image = pyglet.image.load('data/room_60.png')
		floor_image = pyglet.image.load('data/floor_60.png')
		
		bin = pyglet.image.atlas.TextureBin()
		room_texture = bin.add(room_image)
		floor_texture = bin.add(floor_image)	
		
		rows = 30
		columns = 30
		
		for object in self.terrain:
			object.delete()
			
		self.terrain = []
			
		self.batch = pyglet.graphics.Batch()
		
		for i in range(rows):
			for j in range(columns, 0, -1):
				if random.randint(0,1)==1:
					image = room_texture
				else:
					image = floor_texture
				self.terrain.append(ente.Terrain(image, i, j, 
						self.camera_x, self.camera_y, 
						self.tile_width, self.tile_height,
						batch=self.batch))	
		
if __name__ == "__main__":
	# Someone is launching this directly
	keys = key.KeyStateHandler()
	
	space = SpaceGameWindow(keys)
	
	space.push_handlers(keys)

	
	#start the thing
	space.main_loop()