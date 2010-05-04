# -*- coding: utf-8 -*-

from pyglet import *
from pyglet.sprite import Sprite
import pyglet
import random
import main

class Tile(Sprite):
	
	def __init__(self, state, image, coord_x, coord_y, tile_width, tile_height, batch=None):

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
				tile_width, tile_height)
		
		Sprite.__init__(self, image, self.pos_x, self.pos_y, batch=batch)
		
	# expensive function needed for scrolling
	def update_camera(self, camera_x, camera_y):
		self.pos_x = self.pos_x + camera_x
		self.pos_y = self.pos_y + camera_y
		self.set_position(self.pos_x, self.pos_y)
		
	def calc_position(self, coord_x, coord_y, tile_width, tile_height):
		pos_x = (coord_x+coord_y)*tile_width//2
		pos_y = (coord_y-coord_x)*tile_height//2
		return pos_x, pos_y
		
class Person:
	
	def __init__(self, x, y):
		self.x = x
		self.y = y