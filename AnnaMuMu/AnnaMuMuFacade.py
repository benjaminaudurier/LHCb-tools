# =============================================================================
#  @class AnnaMuMuFacade
#  Facade class of the offline analysis framework Anna
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 
import AnnaConfig 

class AnnaMuMuFacade:
	"""
	The framework is meant to work inside the LHCb framework 
	as it relies evely on OSTAP.
	So, prior to import this module, the user must be sure to be 
	in an Ostap session (lb-run Bender/latest ostap).

	This class takes 3 arguments :
		- dataset : file that will be given to Ostap::Data class 
					which contains the datasets paths.

		- chain_list : lists containinf chain(s) name(s) (ex: ["jpsi/DecayTree"]).

		- configfile : read by AnnaConfig to configure 
						our object (See AnnaConfig for details)

	As a facade, each functions call a dedicade class inside the framework when 
	running the task (exp: fit, print diagrams ... ).
	See the classes and functions documentations for more details.
	"""

	## constructor
	def __init__(self, datafile=None, tree=None, configfile=None):

		self._tree
		self._configfile

		# Read file for data pattern 
		pattern = []
		file
		try: 
			file = open(datafile, 'r')
		except:
			print("Cannot read datafile {}".format(datafile))
		
		for line in file:
			pattern.append(line)
		file.close()
		
		# Set _tree with the correct data constructor
		if len(chain_list) == 2:
			self._tree = Data2(chain_list[0], chain_list[1], pattern)

		elif len(chain_list) == 1:
			self._tree = Data2(chain_list[0], pattern)

		else:
			print "Too much chains in {0}, please check it".format(chain_list)
			return

		# Set _configfile 
		if (self._configfile = AnnaConfig(configfile)) is True:
			print "config file set !"

		else:
			print "Cannot set config file"

	def _get_configfile(self):
		return self._configfile

	def _get_tree(self):
		return self._tree

# =============================================================================
# The END 
# =============================================================================
