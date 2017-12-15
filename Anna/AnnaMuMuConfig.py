# =============================================================================
## @class AnnaMuMuConfig
#  helper class to store steering options for other Anna classes 
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 
import os
from logging import debug as debug
from logging import error as error
from logging import warning as warning
from logging import info as info
import copy

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
			lines = file.readlines()

			for key_name in self._key:
				entries = []

				# Find and store all the entries for a given key
				for line in lines:
					info("Reads line {}".format(line))
					if line == '' or line.startswith('#') is True:
						continue
					key, value = self.DecodeLine(line)
					if key == key_name:
						entries.append(value)

				# Add to map
				if len(entries) > 0:
					self._map[key_name] = entries
				else:
					warning("No entries for key {}, set default".format(key_name))
					self._map[key_name] = self.GetDefaultEntry(key_name)

			return True

	# ______________________________________
	def GetCentrality(self):
		return self._map["Centrality"]

	# ______________________________________
	def GetCutCombination(self):
		return self._map["CutCombination"]

	# ______________________________________
	def GetFitType(self):
		return self._map["FitType"]

	# ______________________________________
	def GetLeaf(self):
		return self._map["Leaf"]

	# ______________________________________
	def GetDefaultEntry(self, key_name):
			return "#"
			
	# ______________________________________
	def PrintKey(self):
		print(self._key)

	# ______________________________________
	def PrintMap(self):
		print(self._map)

	# ______________________________________
	def DecodeLine(self, line=""):
		"""  return key and value form the line"""

		split_line = line.replace(" ", "")
		split_line = split_line.strip()
		split_line = split_line.split(":")

		# check the len
		try:
			assert len(split_line) == 2
		except AssertionError:
			print("Format of {} in config file is not correct, should be \"key:values \"".format(line))
			return "", ""

		debug("key: {} / value: {}".format(split_line[0], split_line[1]))
			
		return split_line[0], split_line[1]


# =============================================================================
# The END 
# =============================================================================
