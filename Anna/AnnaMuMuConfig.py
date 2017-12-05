# =============================================================================
## @class AnnaMuMuConfig
#  helper class to store steering options for other Anna classes 
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 

import os

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
			"Cut", 
			"FitType"		
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
					print "Warning: No entries for key {}".format(key_name)
			
			return True

	# ______________________________________
	def GetCentrality(self):
		return self.Map()["Centrality"]

	# ______________________________________
	def GetCut(self):
		return self.Map()["Cut"]

	# ______________________________________
	def GetFitType(self):
		return self.Map()["FitType"]

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
		if len(split_ligne) is not 2:
			print("Error : format of {} in confige file is not correct, should be \"key:values \"".format(ligne))
			return "", ""
		else:
			return split_ligne[0], split_ligne[1]


# =============================================================================
# The END 
# =============================================================================
