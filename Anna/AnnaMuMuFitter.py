# =============================================================================
#  @class AnnaMuMuFitter
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 

from .AnnaMuMuSpectra import AnnaMuMuSpectra
from .AnnaMuMuResult import AnnaMuMuResult
from ROOT import TChain
from ROOT import TH1, TH2

class AnnaMuMuFitter:
	"""helper class for fit process.
	
	This class comes with default binnings that can be set
	differently according to binning 
	"""
	# ______________________________________
	def __init__(self, particle="", binning=[]):
		"""cstr
		
		[description]
		
		Keyword Arguments:
			particle {str} -- use for setting purposes (default: {""})
			binning {list} -- the binning. By convention, binning[0] should
			contain the name of the binning. See AnnaMuMuFitter::DefaultBinning()
			for the possible values (default: {[]})
		"""
		
		# Default binning
		default_binning = self.DefaultBinning()
		self._particle_name = particle		
		# centrality percentage based on VELO cluster cut
		self._centrality = {
			"branch": ["VELOTHITS"] 
			"90_100": [0, 1311],
			"80_90": [1311, 3009],
			"70_80": [3009, 5580],
			"60_70": [5580, 9685],
			"50_60": [9685, 15417],
			"40_50": [15417, 22473]
		}

		# Adopt binning
		self._binning = self.CheckBinning(binning)
		if not self._binning:
			print "Binning is not good ..."
			return
		
	# ______________________________________
	def CheckBinning(self, binning):
		""" Check bining format"""
		
		ok = True

		# Check if binning is known
		if binning[0] not in self.DefaultBinning():
			print("Don't know this binning {} ... \
					Possibles are {}".format(self._binning[0], self.DefaultBinning()))
			ok = False

		# Check binning size
		if (binning[0] == "PT" or binning[0] == "Y") and (len(binning[1:]) < 2):
			print("Not enought bins ({}), required at least 2".format(len(binning[1:])))
			ok = False

		# Check binning ordening
		for i, limit in enumerate(binning[1:]):
			if limit > binning[i + 1]:
				order = False

		if ok is True:
			return binning

		else:
			return None

	# ______________________________________
	def DefaultBinning(self):
		return "INTEGRATED,PT,Y"

	# ______________________________________
	def Fit(self, tchain, leaf_prefix, centrality, cut, fit_type, option):
		"""[summary]
		
		[description]
		
		Arguments:
			tchain {[type]} -- [description]
			leaf_prefix {[type]} -- [description]
			centrality {[type]} -- [description]
			cut {[type]} -- [description]
			fit_type {[type]} -- [description]
			option {[type]} -- [description]
		
		Returns:
			[type] -- [description]
		"""
		# Some needed stuffs
		bintype = self._binning[0] 
		added_result = 0

		# The spectra that will be return
		spectra = AnnaMuMuSpectra(
			name=self._particle_name + "_" + bintype,
			title=self._particle_name + "_" + bintype)

		# Select the process according to bintype
		if bintype == "PT" or bintype == "Y":

			# Loop over bin
			for i in len(self._binning[1:]):
				# Counter
				added_subresult = 0
				# Set the bin limit
				bin_limits = [self._binning[i], self._binning[i + 1]]
				# Get Histo
				histo = self.GetHisto(
					bintype, bin_limits,
					leaf_prefix, centrality, cut)
				# Construct our AnnaMuMuRestult for a given bin
				annaresult = AnnaMuMuResult(
					self._particle_name, histo,
					bintype)

				# Loop over fit method and add fit
				for fit in fit_type:
					added_subresult += annaresult.AddFit(fit) 
				
				added_result += spectra.AdoptResult(annaresult, bin_limits)

			return spectra

		elif bintype == "INTEGRATED":
			fwaef

		else:
			print("Unknown bin type {}".format(bintype))
			return None

	# ______________________________________
	def GetHisto(self, bintype, bin_limits, leaf_prefix, centrality, cut):
		"""[summary]
		
		[description]
		
		Arguments:
			bintype {[type]} -- [description]
			bin_limits {[type]} -- [description]
			leaf_prefix {[type]} -- [description]
			centrality {[type]} -- [description]
			cut {[type]} -- [description]
		"""

		

	# ______________________________________
	def IntegratedPtRange(self):
		return [0., 12.]

	# ______________________________________
	def IntegratedYRange(self):
		return [-4., -2.5]



# =============================================================================
# The END 
# =============================================================================