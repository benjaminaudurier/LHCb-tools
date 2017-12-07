# =============================================================================
## @class AnnaMuMuConfig
#  helper class to store steering options for other Anna classes 
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 

import os
import warnings

class AnnaMuMuConfig:
	""" 
	Holds some options like the fit to be performed, conditions on the kinematices ...
	This class reads an extern text file and store info in a dictionnary. 
	Each line of the config file should be written as <key> : <value> 
	"""

	# ______________________________________
	def __init__(self):	
		""" cstr """
		self._map = dict()
		self._key = (
			"Centrality", 
			"CutCombination", 
			"FitType",
			"Leaf"			
		)

	# ______________________________________
	def ReadFromFile(self, configfile=""):
		""" Read the configuration file and set tuples with correct entries. """

		with open(configfile, "r") as file:
			lignes = file.readlines()

			for key_name in self._key:
				entries = list()

				# Find and store all the entries for a given key
				for ligne in lignes:
					key, value = self.DecodeLine(ligne)
					if key == key_name:
						entries.append(value)

				# Add to map
				if len(entries) > 0:
					self._map[key_name] = tuple(entries)
				else:
					warnings.warn("No entries for key {}, set default".format(key_name))
					self._map[key_name] = self.GetDefaultEntry(key_name)
			
			return True

	# ______________________________________
	def GetCentrality(self):
		return self.Map()["Centrality"]

	# ______________________________________
	def GetCutCombination(self):
		return self.Map()["CutCombination"]

	# ______________________________________
	def GetFitType(self):
		return self.Map()["FitType"]

	# ______________________________________
	def GetLeaf(self):
		return self.Map()["Leaf"]

	# ______________________________________
	def GetDefaultEntry(self, key_name):
		if key_name == "Centrality": 
			return "ALL"
		else:  
			return "None"
			
	# ______________________________________
	def Map(self):
		return self._map.copy()

	# ______________________________________
	def PrintKey(self):
		print self._key

	# ______________________________________
	def PrintMap(self):
		print self._map

	# ______________________________________
	def DecodeLine(self, ligne=""):
		"""  return key and value form the line"""

		ligne.replace(" ", "")
		split_ligne = ligne.split(":")

		# check the len
		try:
			assert len(split_ligne) == 2
		except AssertionError:
			print("Format of {} in config file is not correct, should be \"key:values \"".format(ligne))
			return "", ""
			
		return split_ligne[0], split_ligne[1]


# =============================================================================
# The END 
# =============================================================================
