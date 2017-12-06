# =============================================================================
#  @class AnnaMuMuFacade
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 

from ROOT import TNamed, TObjArray
from .AnnaMuMuResult import AnnaMuMuResult


class AnnaMuMuSpectra(TNamed):
	"""Container for AnnaMuMuResult
	
	AnnaMuMuResults are stored according to a specific binning into a TObjArray.
	
	Extends:
		TName
	"""

	# ______________________________________
	def __init__(self, name, title):
		""" cstr """

		TNamed.__init__(self, name, title)
		self._binning = list()  		# the binning
		self._results = TObjArray()  	# where are stored the AnnaMuMuResults
		self._weight = 1.0  			# results weights

	# ______________________________________
	def AdoptResult(self, result, bin):
		""" adopt (i.e. we are becoming the owner) a result for a given bin"""

		if not result or type(result) != type(AnnaMuMuResult):
			print("Cannot adopt a null result or a non result")
			return False

		# increment binning
		self._binning.append(bin)

		sizeBeforeAdd = self._results.GetEntriesFast()
		self._results.Add(result)  # Add the result to the recently added bin
		sizeAfterAdd = self._results.GetEntriesFast()
		
		if sizeBeforeAdd >= sizeAfterAdd:
			print("Error adopting result {} to spectra {}".format(
				result.GetName(), 
				self._name))
			return False
		
		else: 
			return True

		print "Hello from AdoptResult"

# =============================================================================
# The END 
# =============================================================================
