#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from Ostap.Data import Data 
import AnnaConfig 

class AnnaFacade:
	""" Facade class of the offline analysis framework Anna.
	The framework is meant to work inside the LHCb framework as it relies evely on OSTAP.
	So, prior to import this module, the user must be sure to be in an Ostap session (lb-run Bender/latest ostap).

	This class takes 2 arguments :
		- dataset : file that will be given to Ostap::Data class which contains the datasets paths.
		- configfile : read by AnnaConfig to configure our object (See AnnaConfig for details)

	As a facade, each functions call a dedicade class inside the framework when running the task (exp: fit, print diagrams ... ).
	See the classes and functions documentations for more details.
	"""

	# ============================================================
	def __init__(self, datafile=None, configfile=None):
		""" constructor """

		# Try to read file 
		pattern = []
		file
		try: 
			file = open(datafile, 'r')
		except:
			print("Cannot read datafile {}".format(datafile))
		
		for line in file:
			pattern.append(line)
		file.close()
			

		self._tree = Data('AnnaChain', pattern)
		self._configfile = AnnaConfig(configfile)

	# ============================================================
	def _get_configfile(self):
		return self._configfile


	# ============================================================
	def _get_tree(self):
		return self._tree