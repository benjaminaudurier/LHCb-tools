# =============================================================================
## @class AnnaTupleFilterBase
#  Mother class of all the sparse
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-12-21


class AnnaTupleFilterBase:

	# ______________________________________
	def __init__(self, mother_leaf='', daughter_leafs=['']):
		"""List of the minimal methods for AnnaFilter classes
		For more detailed example, see AnnaTupleFilterJpsiPbPb
		"""
		self.daughter_leafs = daughter_leafs
		self.mother_leaf = mother_leaf
		self.filter_mask = dict()

	# ______________________________________
	def CheckChainBranch(self, chain):
		"""
		Where the user check the chain leafs
		"""
		raise NotImplementedError  # abstract

	# ______________________________________
	def CreateTuple(self):
		"""
		Where the filtered tuple must be created
		and returned
		"""
		raise NotImplementedError  # abstract

	# ______________________________________
	def GetGeneralMask(self):
		"""
		Return the general cut masks
		to be applied before running over
		Chain events

		Returns:
			[str] -- [description]
		"""
		raise NotImplementedError  # abstract

		# ______________________________________
	def GetTuple(self, chain):
		"""The main method of the class

		Here the class run in all events in the tree/chain
		and return a filled new tuple for events passing the
		selection

		Arguments:
			chain {TChain}

		Returns:
			TNtuple
		"""
		raise NotImplementedError  # abstract


# =============================================================================
# The END
# =============================================================================
