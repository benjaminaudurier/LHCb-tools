# =============================================================================
#  @class AnnaMuMuFacade
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 

from ROOT import TObject

class AnnaMuMuResult(TObject):
	"""[summary]
	
	[description]
	
	Extends:
		TObject
	"""

	def __init__(self, arg):
		self.arg = arg
