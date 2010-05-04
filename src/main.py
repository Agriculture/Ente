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
	screen_height = 400
	
	tile_width = 60
	tile_height = 40
	
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
		
		# pack all images in one bin
		# so they stay inorder
		bin = pyglet.image.atlas.TextureBin()
		room_texture = bin.add(room_image)
		floor_texture = bin.add(floor_image)
		self.transparent_texture = bin.add(transparent_image)
		self.monster_texture = bin.add(monster_image)
		
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
						self.tile_width, self.tile_height,
						batch=self.batch))	
				line2.append(ente.Tile("nonoccupied", self.transparent_texture, i, j, 
						self.tile_width, self.tile_height,
						batch=self.batch))	

	def init_hero(self):
		check = True
		while check:
			hero_x = random.randint(0, self.rows - 1)
			hero_y = random.randint(0, self.columns - 1)
			if (self.background[hero_x][hero_y].state == "accessible"):
				check = False

		# find the hero ;)
		# we created the columns backwards, so (columns - y)
		# plus the half of the screen
		self.camera_x = - (hero_x + (self.columns - hero_y)) * self.tile_width//2 + self.screen_width//2
		self.camera_y = - ((self.columns - hero_y) - hero_x) * self.tile_height//2 + self.screen_height//2
		print self.camera_x, self.camera_y
		self.update_camera()

		self.foreground[hero_x][hero_y].image = self.monster_texture
		self.characters = []
		self.characters.append(ente.Person(hero_x, hero_y))

	def move_hero(self, x, y):
		old_x = self.characters[0].x
		old_y = self.characters[0].y

		new_x = old_x + x
		new_y = old_y + y
		
		# out of screen?
		if(new_x < 0 or new_y < 0 or new_x >= self.rows or new_y >= self.columns):
			return

		# place blocked?
		if(self.background[new_x][new_y].state == "nonaccessible"):
			return
		
		foreground[old_x][old_y].image = self.transparent_texture
		foreground[new_x][new_y].image = self.monster_image

if __name__ == "__main__":
	# Someone is launching this directly
	keys = key.KeyStateHandler()

	space = SpaceGameWindow(keys)

	space.push_handlers(keys)

	#start the thing
	space.main_loop()