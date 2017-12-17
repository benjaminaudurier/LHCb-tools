# =============================================================================
#  @class AnnaMuMuFacade
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 

from ROOT import TNamed, TObjArray
from .AnnaMuMuResult import AnnaMuMuResult
from logging import debug as debug
from logging import error as error
from logging import warning as warning


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
		self._results = dict()  	# where are stored the AnnaMuMuResults
		self._weight = 1.0  		# results weights

	# ______________________________________
	def AdoptResult(self, result, bin):
		""" adopt (i.e. we are becoming the owner) a result for a given bin"""

		if result is None:
			error("AdoptResult: Cannot adopt a null result list")
			return 0

		debug("AdoptResult: result : {}".format(result))
		sizeBeforeAdd = len(self._results)
		self._results[str(bin)] = result  # Add the result for a given bin type
		sizeAfterAdd = len(self._results)
			
		if sizeBeforeAdd >= sizeAfterAdd:
			error("AdoptResult: Error adopting result {} to spectra {}".format(
				result.GetName(), 
				self.GetName()))
			return 0
		
		else: 
			print(" --- result {} adopted !".format(result.GetName(), sizeAfterAdd - sizeBeforeAdd))
			return 1


# =============================================================================
# The END 
# =============================================================================
