# =============================================================================
#  @class AnnaMuMuFacade
# 
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
	def __init__(self, name=""):
		""" cstr """

		self._binning = tuple()  # the binning
		self._results = TObjArray()  # where are stored the AnnaMuMuResults
		self._weight = list()  # results weights
		self._name = name  # Name

	# ______________________________________
	def AdoptResult(self, result):
		""" adopt (i.e. we are becoming the owner) a result for a given bin"""

		if not result or type(result) != type(AnnaMuMuResult):
			print("Cannot adopt a null result or a non result")
			return False

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
