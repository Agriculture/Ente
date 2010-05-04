# -*- coding: utf-8 -*-
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
	
	scroll_speed = 10
	
	rows = 30
	columns = 30

	def __init__(self, keys, *args, **kwargs):
		self.keys = keys
		#Let all of the standard stuff pass through
		window.Window.__init__(self, width=self.screen_width,
			height=self.screen_height, *args, **kwargs)
		self.init_objects()
		
	def init_objects(self):
							
		self.stupid()
		self.init_hero()


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
		self.camera_x = 0
		self.camera_y = 0
		if self.keys[key.RIGHT]:
			space.camera_x = -self.scroll_speed
			space.update_camera()	
		if self.keys[key.LEFT]:
			space.camera_x = self.scroll_speed
			space.update_camera()	
		if self.keys[key.DOWN]:
			space.camera_y = self.scroll_speed
			space.update_camera()	
		if self.keys[key.UP]:
			space.camera_y = -self.scroll_speed
			space.update_camera()
		
	def update_camera(self):
		for line in self.background:
			for object in line:
				object.update_camera(self.camera_x, self.camera_y)
		for line in self.foreground:
			for object in line:
				object.update_camera(self.camera_x, self.camera_y)
		
	def stupid(self):	
		room_image = pyglet.image.load('data/room_60.png')
		floor_image = pyglet.image.load('data/floor_60.png')
		transparent_image = pyglet.image.load('data/transparent_60.png')
		monster_image = pyglet.image.load('data/monster_60.png')
		
		bin = pyglet.image.atlas.TextureBin()
		room_texture = bin.add(room_image)
		floor_texture = bin.add(floor_image)
		transparent_texture = bin.add(transparent_image)
		self.monster_texture = bin.add(monster_image)
		
		#init the camera to the middle of the board, not important
		self.camera_x = -13 * self.tile_width
		self.camera_y = 6 * self.tile_height
		
		self.background = []
		self.foreground = []
		
		self.batch = pyglet.graphics.Batch()
		
		for i in range(self.rows):
			line1 = []
			line2 = []
			self.background.append(line1)
			self.foreground.append(line2)
			for j in range(self.columns, 0, -1):
				if random.randint(0,1)==1:
					image = room_texture
					state = "nonaccessible"
				else:
					image = floor_texture
					state = "accessible"
				line1.append(ente.Tile(state, image, i, j, 
						self.camera_x, self.camera_y, 
						self.tile_width, self.tile_height,
						batch=self.batch))	
				line2.append(ente.Tile("nonoccupied", transparent_texture, i, j, 
						self.camera_x, self.camera_y, 
						self.tile_width, self.tile_height,
						batch=self.batch))	

	def init_hero(self):
		check = True
		while check:
			hero_x = random.randint(0, self.rows)
			hero_y = random.randint(0, self.columns)
			if (self.background[hero_x][hero_y].state == "accessible"):
				check = False
		self.foreground[hero_x][hero_y].image = self.monster_texture

if __name__ == "__main__":
	# Someone is launching this directly
	keys = key.KeyStateHandler()

	space = SpaceGameWindow(keys)

	space.push_handlers(keys)

	#start the thing
	space.main_loop()