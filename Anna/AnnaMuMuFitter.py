# =============================================================================
#  @class AnnaMuMuFacade
#  helper class for fit process.
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 


class AnnaMuMuFitter:
	"""helper class for fit process.
	
	This class comes with default binnings that can be set
	differently according to binning 
	"""
	# ______________________________________
	def __init__(self, particle, binning):
		"""cstr 
		
		Keyword Arguments:
			particle {str} -- [description] (default: {""})
			binning {str || list} -- If a str, select default binning.
									Pass a list to change the default binning where
									binning[0] is the name of the binning and binning[1]...binning[n]
									are the binning boundaries.
		"""
		
		# Default binning
		default_binning = "pt,y"
		default_integrated = [0, 12, -4.00, -2.50]
		default_pt = [0, 1, 2, 3, 4, 5, 6, 8, 10]
		default_y = [-4, -3.75, -3.50, -3.25, -3.0, -2.75, -2.5]

		self._particle_name = particle
		
		# centrality percentage based on VELO cluster cut
		self._centrality = {
			"90_100": [0, 1311],
			"80_90": [1311, 3009],
			"70_80": [3009, 5580],
			"60_70": [5580, 9685],
			"50_60": [9685, 15417],
			"40_50": [15417, 22473]
		}
		self._binning = []

		# Select default binning
		if type(binning) is str:
			if binning == "pt":
				self._binning = default_pt
			elif binning == "y":
				self._binning = default_y
			elif binning == "integrated":
				self._binning = default_integrated
			else:
				print("Binning {} unknown, expect something bad \
					to happen ....".format(binning))

		elif type(binning) is list:
			self._binning = binning
			if self._binning[0] not in default_binning:
				print("Don't know this binning {} ... \
					Expect something bad to happen".format(self._binning[0]))
		else:
			print("Type of {} is {}, expect str() \
				of list()".format(binning, type(binning)))

	# ______________________________________
	def Fit(self, centrality="", cut="", fit_type="", option=""):
		"""Fit the invariante mass spectrum.
		
		Fit results are given in the form of AnnaMuMuResuts for each bins.
		They are stored in an AnnaMuMuSpectra class created and returned
		by the present method.
		
		Keyword Arguments:
			centrality {str} -- centrality cut (default: {""})
			cut {str} -- cuts on the leaf (default: {""})
			fit_type {str} -- configure the fit function (default: {""})
			option {str} -- (default: {""})
		"""







# =============================================================================
# The END 
# =============================================================================