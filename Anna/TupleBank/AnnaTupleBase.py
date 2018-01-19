# =============================================================================
## @class AnnaTupleBase
#  Mother class of all the sparse
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-12-21

from logging import error, warning,info

class AnnaTupleBase:

	# ______________________________________
	def __init__(self, mother_leaf='', dimuon_leafs=['', ''], name=''):
		"""List of the minimal data members requiered

		The filter_mask of daughter class should be of the form:

		self.filter_mask =
		{
			'muon_mask': 'cut1**cut2**...**cutn',
			'mother_mask': 'cut1**cut2**...**cutn',
			'other': 'cut1**cut2**...**cutn'
		}

		Note that by conventions, the variable (or branch) name must be
		written before the condition. Also by convention :
			dimuon_leafs[0] = mu_plus
			dimuon_leafs[1] = mu_minus

		exemple :
			"mother_mask": 'Y  < 4.5 ** Y > 2.0 ** MM < 3196.900 ** MM > 2996.900'
		For more detailed example, see AnnaSparseJpsiPbPb

		Arguments:
			name {str}
		"""
		self.dimuon_leafs = dimuon_leafs
		self.filter_mask = {
			'muon_mask': '',
			'mother_mask': '',
			'other': ''}
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
			error("AnnaTupleBase:GetGeneralMask: no filter mask !")
			return None

		# Get masks
		general_mask = ''
		if self.filter_mask['muon_mask'] != '':
			for leaf in self.dimuon_leafs:
				for cut in self.filter_mask['muon_mask'].split('**'):
					general_mask += '{}_{}&&'.format(leaf, cut)

		if self.filter_mask['mother_mask'] != '':
			for cut in self.filter_mask['mother_mask'].split('**'):
					general_mask += '{}_{}&&'.format(self.mother_leaf, cut)

		if self.filter_mask['other'] != '':
			for cut in self.filter_mask['other'].split('**'):
					general_mask += '{}&&'.format(cut)

		return str(general_mask[:-2]).replace(" ", "")

		# ______________________________________
	def GetTuple(self, chain):
		raise NotImplementedError  # abstract

	# ______________________________________
	def PassMuonCuts(self, entry_number, entry):
		"""
		Check muons angle to see if not ghost particule

		Returns:
			Bool
		"""

		for leaf in self.dimuon_leafs:
			for cut in self.filter_mask['muon_mask'].replace(' ', '').split('**'):
				suporinf = '>' if '>' in cut else '<'
				att_name = cut.split(suporinf)[0]
				try:
					attribute = getattr(entry, str(leaf + '_' + att_name))
				except AttributeError:
					warning(
						"No info {}_{} in entry {}"
						.format(leaf, att_name, entry_number))
					return False

				if suporinf == '>' and attribute > float(cut.split(suporinf)[1]):
					continue
				elif suporinf == '<' and attribute < float(cut.split(suporinf)[1]):
					continue
				else:
					info(
						" {}_{} = {:.2f} (cut : {}{:.2f})"
						.format(
							leaf,
							att_name,
							attribute,
							suporinf,
							float(cut.split(suporinf)[1])))
					return False

		return True

	# ______________________________________
	def PassMotherCuts(self, entry_number, entry):
		"""
		Check muons angle to see if not ghost particule

		Returns:
			Bool
		"""

		for cut in self.filter_mask['mother_mask'].replace(' ', '').split('**'):
			suporinf = '>' if '>' in cut else '<'
			att_name = cut.split(suporinf)[0]
			try:
				attribute = getattr(entry, str(self.mother_leaf + '_' + att_name))
			except AttributeError:
				warning(
					"No info {}_{} in entry {}"
					.format(self.mother_leaf, att_name, entry_number))
				return False

			if suporinf == '>' and attribute > float(cut.split(suporinf)[1]):
				continue
			elif suporinf == '<' and attribute < float(cut.split(suporinf)[1]):
				continue
			else:
				info(
					" {}_{} = {:.2f} (cut : {}{:.2f}) "
					.format(
						self.mother_leaf,
						att_name,
						attribute,
						suporinf,
						float(cut.split(suporinf)[1])))
				return False

		return True


# =============================================================================
# The END
# =============================================================================
