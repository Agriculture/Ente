# -*- coding: utf-8 -*-

from pyglet import *
from pyglet.sprite import Sprite
import pyglet
import random
import main

class Tile(Sprite):
	
	def __init__(self, state, image, coord_x, coord_y, camera_x, camera_y, tile_width, tile_height, 
		batch=None):

		""" state:
		accessible		(floor)
		nonaccessible		(cube)
		occupied		(monster, hero)
		nonoccupied		(transparent image)
		"""
		self.state = state
		
		self.coord_x = coord_x
		self.coord_y = coord_y
		
		self.pos_x, self.pos_y = self.calc_position(coord_x, coord_y, 
				tile_width, tile_height, camera_x, camera_y)
		
		Sprite.__init__(self, image, self.pos_x, self.pos_y, batch=batch)
		
	# expensive function needed for scrolling
	def update_camera(self, camera_x, camera_y):
		self.pos_x = self.pos_x + camera_x
		self.pos_y = self.pos_y + camera_y
		self.set_position(self.pos_x, self.pos_y)
		
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
		