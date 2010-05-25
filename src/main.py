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
	
	# one thingy on the map
	tile_width = 60
	tile_height = 40
	
	# basicly the size of the map
	rows = 30
	columns = 30

	def __init__(self, keys, *args, **kwargs):
		self.keys = keys
		#Let all of the standard stuff pass through
		window.Window.__init__(self, width=self.screen_width,
			height=self.screen_height, *args, **kwargs)
		self.init_objects()

		self.move_available = 0
		
	def init_objects(self):
							
		self.init_map()
		self.init_hero()


	def draw(self):
		self.batch.draw()

	def main_loop(self):
		while not self.has_exit:
			self.dispatch_events()
			self.clear()

			#clocke is needed for fps
			clock.tick()
			
			#also handles the key events if needed
			self.check_keys()
				
			#Gets fps and make it visible
			self.set_caption("fps: "+str(round(clock.get_fps())))
			
			# updates the map
			self.draw()

			#update the screen
			self.flip()


	def check_keys(self):

		move_x = 0
		move_y = 0
		action = False
		if self.keys[key.RIGHT]:
			move_x = 1
			action = True
		elif self.keys[key.LEFT]:
			move_x = -1
			action = True
		elif self.keys[key.UP]:
			move_y = 1
			action = True
		elif self.keys[key.DOWN]:
			move_y = -1
			action = True

		#if it would always available it would be too fast
		if(action and (self.move_available <= 0)):
				self.move_hero(move_x, move_y)
				self.move_available = 0.5
		else:
			# decrease it wrt. to fps (if possible)
			if(clock.get_fps() > 0):
				self.move_available -= 1/clock.get_fps()

			
		
	def update_camera(self):
		for line in self.background:
			for object in line:
				object.update_camera(self.camera_x, self.camera_y)
		for line in self.foreground:
			for object in line:
				object.update_camera(self.camera_x, self.camera_y)
		
	def init_map(self):	
		# every point on the map has a background_image
		# only if this point is occupied there is a foreground_image
		# if unoccupied there is a transparent_image which can be replaced
		# (so all images stay inorder)
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
				if random.randint(0,4)==1:
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
		self.update_camera()

		# print the texture of the hero in the foreground
		self.foreground[hero_x][hero_y].image = self.monster_texture
		self.characters = []
		self.characters.append(ente.Person(hero_x, hero_y))

	def move_hero(self, x, y):
		hero = self.characters[0]
		old_x = hero.x
		old_y = hero.y

		# columns are backwards
		new_x = old_x + x
		new_y = old_y - y
		
		# out of screen?
		if(new_x < 0 or new_y < 0 or new_x >= self.rows or new_y >= self.columns):
			return

		# place blocked?
		if(self.background[new_x][new_y].state == "nonaccessible"):
			return
		
		hero.x = new_x
		hero.y = new_y

		self.foreground[old_x][old_y].image = self.transparent_texture
		self.foreground[new_x][new_y].image = self.monster_texture

#		self.camera_x = (y + x) * self.tile_width//2
#		self.camera_y = (y + x) * self.tile_height//2
#		self.update_camera()


if __name__ == "__main__":
	# Someone is launching this directly
	keys = key.KeyStateHandler()

	space = SpaceGameWindow(keys)

	space.push_handlers(keys)

	#start the thing
	space.main_loop()