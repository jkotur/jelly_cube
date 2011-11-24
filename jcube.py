
from OpenGL.GL import *
from OpenGL.GLU import *

import math as m
import numpy as np
import random as rnd

import cjelly
from drawable import Drawable

class JellyCube( Drawable ) :
	SHAPE = (4,4,4)
	C = 0.01
	K = 2.0

	def __init__( self ) :
		self.pts = np.zeros( (self.SHAPE[0],self.SHAPE[1],self.SHAPE[2],3) , np.float64 )
		self.prv = np.zeros( (self.SHAPE[0],self.SHAPE[1],self.SHAPE[2],3) , np.float64 )
		self.pl = np.zeros( (self.SHAPE[0],self.SHAPE[1],self.SHAPE[2],3) , np.float64 )
		self.nl = np.zeros( (self.SHAPE[0],self.SHAPE[1],self.SHAPE[2],3) , np.float64 )
		self.mas = np.ones ( (self.SHAPE[0],self.SHAPE[1],self.SHAPE[2],3) , np.float64 )
		self.l0 = 1
		self.l1 = m.sqrt(2) * self.l0

		self.__pts_aligned( self.l0 )
		self.__func( self.prv , lambda x,y,z : self.pts[x,y,z] )
		self.__func( self.pl  , lambda x,y,z : 0 )
		self.__func( self.mas , lambda x,y,z : 10 )
#        self.pts[2,3,2,1] += .5
#        self.prv[2,3,2,1] += .5

		self.t = -3

	def __pts_aligned( self , s ) :
		for x in range(self.SHAPE[0]) :
			for y in range(self.SHAPE[1]) :
				for z in range(self.SHAPE[2]) :
					self.pts[x,y,z] = np.array((x,y,z)) * s

	def __func( self , p , f ) :
		for x in range(self.SHAPE[0]) :
			for y in range(self.SHAPE[1]) :
				for z in range(self.SHAPE[2]) :
					p[x,y,z] = f( x,y,z )

	def gfx_init( self ) :
		pass

	def draw( self ) :
		glPointSize( 5 )
		glBegin(GL_POINTS)
		for x in range(self.SHAPE[0]) :
			for y in range(self.SHAPE[1]) :
				for z in range(self.SHAPE[2]) :
					glColor3f(x/4.0 , y/4.0 , z/4.0 )
					glVertex3f( *self.pts[x,y,z] )
		glEnd()


	def wobble( self , dt ) :
		self.t += dt 
		if self.t < 0 : return 

		cjelly.springs( self.pts , self.nl , self.l0 , self.l1 )
		cjelly.update( self.pts , self.prv , self.pl , self.nl , self.mas , self.K ,self.C , dt )

