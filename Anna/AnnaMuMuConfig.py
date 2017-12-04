# =============================================================================
## @class AnnaMuMuConfig
#  helper class to store steering options for other Anna classes 
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 

class AnnaMuMuConfig:
	""" 
	Holds some options like the fit to be performed, conditions on the kinematices ...
	This class reads an extern file config.anna. 
	Each line should be written as <key> : <value> <type> 
	"""

	## constructor
	def __init__(self):
		print("coucou le constructeur")


	def ReadFromFile(self, configfile=None):
		
		print "Coucou !"
		return True

# =============================================================================
# The END 
# =============================================================================
