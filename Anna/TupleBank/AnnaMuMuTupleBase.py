# =============================================================================
## @class AnnaMuMuTupleBase
#  Mother class of all the sparse
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-12-21 

from logging import error

class AnnaMuMuTupleBase:

	# ______________________________________
	def __init__(self, mother_leaf='', dimuon_leafs=['', ''], name=''):
		"""List of the minimal data members requiered

		The filter_mask of daughter class should be of the form:

		self.filter_mask =
		{
			'muon_mask': 'cut1|cut2|...|cutn',
			'mother_mask': 'cut1|cut2|...|cutn',
			'other': 'cut1|cut2|...|cutn'
		}

		For example, see AnnaMuMuSparseJpsiPbPb
				
		Arguments:
			name {str} -- 
		"""
		self.dimuon_leafs = dimuon_leafs
		self.filter_mask = None
		self.mother_leaf = mother_leaf
		self.name = name

	# ______________________________________
	def CheckChainBranch(self, chain):
		raise NotImplementedError  # abstract

	# ______________________________________
	def CreateTuple(self):
		raise NotImplementedError  # abstract

	# ______________________________________
	def GetGeneralMask(self):

		if self.filter_mask is None:
			error("AnnaMuMuTupleBase:GetGeneralMask: no filter mask !")
			return None

		# Get masks
		general_mask = ''
		if self.filter_mask['muon_mask'] != '': 
			for leaf in self.dimuon_leafs:
				for cut in self.filter_mask['muon_mask'].split('|'):
					general_mask += '{}_{}&&'.format(leaf, cut)

		if self.filter_mask['mother_mask'] != '': 
			for cut in self.filter_mask['mother_mask'].split('|'):
					general_mask += '{}_{}&&'.format(self.mother_leaf, cut)

		if self.filter_mask['other'] != '': 
			for cut in self.filter_mask['other'].split('|'):
					general_mask += '{}&&'.format(cut)

		return general_mask[:-2]

		# ______________________________________
		def GetTuple(self, chain):
			raise NotImplementedError  # abstract

# =============================================================================
# The END 
# =============================================================================