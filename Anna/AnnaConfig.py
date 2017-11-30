#!/usr/bin/env python 
# -*- coding: utf-8 -*-

class AnnaConfig:
	""" helper class to store steering options for other Anna classes
	Holds some options like the fit to be performed, conditions on the kinematices ...
	This class reads an extern file config.anna. 
	Each line should be written as <key> : <value> <type> 
	"""

	# ============================================================
	def __init__(self, configfile=None):
