# =============================================================================
#  @class AnnaMuMuFacade
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 

from ROOT import TNamed, TObjArray
from logging import debug as debug
from logging import error as error



class AnnaMuMuSpectra():
	"""Container for AnnaMuMuResult
	
	AnnaMuMuResults are stored according to a specific binning into a TObjArray.
	
	Extends:
		TNamed
	"""

	# ______________________________________
	def __init__(self, name, title):
		""" cstr """

		self.name = name 
		self.title = title
		self._results = dict()  	# where are stored the AnnaMuMuResults

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
			print(" --- result {} adopted !".format(result.GetName()))
			return 1

	# ______________________________________
	def GetName(self):
		return self.name

	# ______________________________________
	def GetTitle(self):
		return self.title


# =============================================================================
# The END 
# =============================================================================
