# =============================================================================
#  @class AnnaMuMuFitter
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 

from .AnnaMuMuSpectra import AnnaMuMuSpectra
from .AnnaMuMuResult import AnnaMuMuResult
from ROOT import TChain
from ROOT import TH1F, TH2F

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
			"branch": ["VELOTHITS"], 
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
		""" Check binning format"""
		
		ok = True
		2D = False

		#Check size
		try:
			assert len(binning) > 2
		except AssertionError:
			print "binning is too small"
			ok = False

		# Check if 2D binning
		if len(binning[0]) > 2:
			if len(binning[1]) > 2:
				print ' --- Fit with a 2D binning {}-{}'.format(binning[0][0],
																binning[1][0])
				2D = True

		# Further checks for 1D binning
		if 2D is not True:
			# Check if binning is known
			try:
				assert binning[0] in self.DefaultBinning()
			except AssertionError:
				print("Don't know this binning {} ... \
				Possibles are {}".format(self._binning[0], self.DefaultBinning()))
				ok = False

			# Check binning size
			if (binning[0] == "PT" or binning[0] == "Y") and ok is True:
				try:
					assert len(binning[1:]) < 2
				except AssertionError:
					print("Not enought bins ({}), \
					required at least 2".format(len(binning[1:])))
					ok = False

			# Check binning ordening
			if ok is True:
				for i, limit in enumerate(binning[1:]):
					try:
						assert limit < binning[i + 1]
					except AssertionError:
						print " --Binning not order properly"
						ok = False
		else:
			# Check if binning is known
			try:
				assert binning[0][0] in ['PT', 'Y']
			except AssertionError:
				print("Don't know this binning {} ... \
				Possibles are {}".format(self._binning[0][0], self.DefaultBinning()))
				ok = False
			try:
				assert binning[1][0] in ['PT', 'Y']
			except AssertionError:
				print("Don't know this binning {} ... \
				Possibles are {}".format(self._binning[1][0], self.DefaultBinning()))
				ok = False

			# Check binning size
			if ok is True:
				try:
					assert len(binning[0][1:]) < 2
				except AssertionError:
					print("Not enought bins ({}), \
					required at least 2".format(len(binning[0][1:])))
					ok = False
				try:
					assert len(binning[!][1:]) < 2
				except AssertionError:
					print("Not enought bins ({}), \
					required at least 2".format(len(binning[!][1:])))
					ok = False

			# Check binning ordening
			if ok is True:
				for i, limit in enumerate(binning[0][1:]):
					try:
						assert limit < binning[0][i + 1]
					except AssertionError:
						print " --- Binning not order properly"
						ok = False
				for i, limit in enumerate(binning[1][1:]):
					try:
						assert limit < binning[0][i + 1]
					except AssertionError:
						print " --- Binning not order properly"
						ok = False

		try:
			assert ok is True
		except AssertionError:
			print "Binning is wrong"
			return None

		return binning
		
	# ______________________________________
	def DefaultBinning(self):
		return "INTEGRATED,PT,Y"

	# ______________________________________
	def Fit(self, tchain, leaf, centrality, cuts, fit_type, option):
		"""[summary]
		
		[description]
		
		Arguments:
			tchain {[type]} -- [description]
			leaf {[type]} -- [description]
			centrality {[type]} -- [description]
			cuts {[type]} -- [description]
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
					tchain, bintype, bin_limits,
					leaf, centrality, cuts)
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
			print "To be implemented"

		else:
			print("Unknown bin type {}".format(bintype))
			return None

	# ______________________________________
	def GetHisto(self, tchain, bintype, bin_limits, leaf, centrality, cuts):
		"""[summary]
		
		[description]
		
		Arguments:
			bintype {[type]} -- [description]
			bin_limits {[type]} -- [description]
			leaf {[type]} -- [description]
			centrality {[type]} -- [description]
			cuts {[type]} -- [description]
		"""
	
		ok_leaf = self.CheckLeafName(tchain, leaf)

		try:
			assert ok_leaf is True
		except AssertionError:
			print("Cannot find leaf {}".format(leaf))
			return None

		tchain.Draw("{}>>histo".format(leaf), cuts, "goff")

		histo = tchain.GetHistogram()

		try:
			assert histo is not None
		except AssertionError:
			print("Cannot get histo from leaf {}".format(leaf))
			return None

		return histo



		

	# ______________________________________
	def IntegratedPtRange(self):
		return [0., 12.]

	# ______________________________________
	def IntegratedYRange(self):
		return [-4., -2.5]



# =============================================================================
# The END 
# =============================================================================