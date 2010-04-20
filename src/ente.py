from pyglet import *
from pyglet.sprite import Sprite
import pyglet
import random
import main

class Terrain(Sprite):
	
	def __init__(self, image, coord_x, coord_y, camera_x, camera_y, 
		screen_width, screen_height, tile_width, tile_height, 
		batch=None, group=None):
		
		self.coord_x = coord_x
		self.coord_y = coord_y
		
		pos_x, pos_y = self.calc_position(coord_x, coord_y, 
				tile_width, tile_height, camera_x, camera_y)
		
		#check if it needs to be rendered
		if(self.out_of_screen(pos_x, pos_y,screen_width, screen_height, 
				tile_width, tile_height)):
			batch=None
		
		Sprite.__init__(self, image, pos_x, pos_y, batch=batch, group=group)
		
	# expensive function needed for scrolling
	def update_camera(self, camera_x, camera_y, screen_width, screen_height,
			tile_width, tile_height, batch=None):	
		pos_x, pos_y = self.calc_position(self.coord_x, self.coord_y, 
				tile_width, tile_height, camera_x, camera_y)
		
		if(self.out_of_screen(pos_x, pos_y, screen_width, screen_height, 
				tile_width, tile_height)):
			batch=None
			
		self.set_position(pos_x, pos_y)
		self.batch=batch
		
	def out_of_screen(self, pos_x, pos_y, screen_width, screen_height, 
			tile_width, tile_height):
		return (	(pos_y > screen_height)
			or 	(pos_x > screen_width)
			or 	(pos_y < -tile_height*1.5) #TODO: not enough, but looks cool
			or 	(pos_x < -tile_width)	)
		
	def calc_position(self, coord_x, coord_y, tile_width, tile_height, camera_x, camera_y):
		pos_x = (coord_x+coord_y)*tile_width//2 + camera_x
		pos_y = (coord_y-coord_x)*tile_height//2 + camera_y
		return pos_x, pos_y
		
	
	"""
	def move(self, direction, step=1):
		dict ={	'Up':	(0, -1),
			'Down':	(0, 1),
			'Left':	(-1, 0),
			'Right':(1, 0)	}
		(i, j) = dict[direction]
		self.x = self.x + i*step
		self.y = self.y + j*step
		self.set_position(self.x, self.y)
		"""	