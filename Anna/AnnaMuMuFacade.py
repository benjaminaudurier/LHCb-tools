# =============================================================================
#  @class AnnaMuMuFacade
#  Facade class of the offline analysis framework Anna
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 
from .AnnaMuMuConfig import AnnaMuMuConfig as AnnaMuMuConfig
from ROOT import TChain 

class AnnaMuMuFacade:
	"""
	The framework is meant to work inside the LHCb framework 
	as it relies evely on OSTAP.
	So, prior to import this module, the user must be sure to be 
	in an Ostap session (lb-run Bender/latest ostap).

	This class takes 3 arguments :
		- tchain : A first TChain object containing the data.
		
		- tchain2 : A second TChain object, not medatory, but usefull in MC studies for instance.

		- configfile : read by AnnaConfig to configure 
						our object (See AnnaConfig for details)

	As a facade, each functions call a dedicade class inside the framework when 
	running the task (exp: fit, print diagrams ... ).
	See the classes and functions documentations for more details.
	"""

	## constructor
	def __init__(self, tchain=None, tchain2=None, configfile=""):

		self._tchain = tchain
		self._tchain2 = tchain2
		self._configfile = AnnaMuMuConfig()
		
		if self._tchain is not None and type(self._tchain) is not TChain:
			print("{} is not a TChain".format(tchain))
			return

		if self._tchain2 is not None and type(self._tchain2) is not TChain:
			print("{} is not a TChain".format(tchain2))
			return

		# Set _configfile 
		if self._configfile.ReadFromFile(configfile) is True:
			print "config file set !"

		else:
			print "Cannot set config file"

	# ______________________________________
	def __str__(self):
		return "I am your father"
				
	# ______________________________________
	def FitParticle(self, particle_name="jpsi"):
		return

	# ______________________________________
	def DrawMinv(self, particle_name="jpsi"):
		return

	# ______________________________________
	def DrawFitResults(self, particle_name="jpsi"):
		return

	# ______________________________________
	def DrawNofWhat(self, particle_name="jpsi"):
		return

	# ______________________________________
	def SaveResults(self, AnnaMuMuResults):
		return

# =============================================================================
# The END 
# =============================================================================
