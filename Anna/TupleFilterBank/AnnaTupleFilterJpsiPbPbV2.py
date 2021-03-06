# =============================================================================
## @class AnnaTupleFilterBase
#  Mother class of all the sparse
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-12-21

from logging import error, info
from .AnnaTupleFilterBase import AnnaTupleFilterBase
from ROOT import TNtuple, TVector3, TMath, TLorentzVector
from Ostap.PyRoUts import *
from Ostap.progress_bar import ProgressBar

# ______________________________________
class AnnaTupleFilterJpsiPbPbV2(AnnaTupleFilterBase):

	# ______________________________________
	def __init__(self, mother_leaf='', dimuon_leafs=['', '']):
		"""THnSparse for Jpsi PbPb Analysis

		Keyword Arguments:
			mother_leaf {str} -- (default: {''})
			dimuon_leafs {list} -- (default: {[''})
			name {str} -- (default: {''})
		"""

		AnnaTupleFilterBase.__init__(
			self,
			mother_leaf,
			dimuon_leafs,
			'AnnaTupleFilterJpsiPbPbV2')

		self.filter_mask["daughter_mask"] = 'TRACK_GhostProb<0.5'\
			'** ProbNNghost<0.8 ** TRACK_CHI2NDOF<3.'\
			'** IP_OWNPV<3.** PIDmu > 0 ** ETA < 4.5 ** ETA > 2.0 '
		self.filter_mask["mother_mask"] = ''

	# ______________________________________
	def CheckChainBranch(self, chain):
		"""Make sure the chain has the requiered leafs
		Arguments:
			chain {TChain} --
		"""

		# vertex info
		for axis in ['X', 'Y', 'Z']:
			try:
				assert str(self.mother_leaf + '_OWNPV_' + axis) \
					in chain.GetListOfBranches()
			except AssertionError:
				error(
					" No info {}_OWNPV_{} branch in chain"
					.format(self.mother_leaf, axis))
				return False
			try:
				assert str(self.mother_leaf + '_ENDVERTEX_' + axis) \
					in chain.GetListOfBranches()
			except AssertionError:
				error(
					" No info {}_ENDVERTEX_{} branch in chain"
					.format(self.mother_leaf, axis))
				return False

		# mother info
		for attr in ['_MM', '_PT', '_Y']:
			try:
				assert str(self.mother_leaf + attr) in chain.GetListOfBranches()
			except AssertionError:
				error(" No info {}_{} branch in chain".format(self.mother_leaf, attr))
				return False

		# dimuon info
		for muon in self.dimuon_leafs:
			for attr in ['_PIDmu', '_CosTheta', '_PIDK', '_ETA']:
				try:
					assert str(muon + attr) in chain.GetListOfBranches()
				except AssertionError:
					error(" No info {}_{} branch in chain".format(muon, attr))
					return False

			for axis in ['X', 'Y', 'Z', 'E']:
				try:
					assert str(muon + '_P' + axis) \
						in chain.GetListOfBranches()
				except AssertionError:
					error(" No info {}_P{} branch in chain".format(muon, axis))
					return False

		# other
		for attr in ['eHcal', 'eEcal']:
			try:
				assert attr in chain.GetListOfBranches()
			except AssertionError:
				error(" No info {} branch in chain".format(attr))
				return False

		return True

	# ______________________________________
	def CreateTuple(self):

		return TNtuple(
			self.name,
			self.name,
			"MM:PT:Y:Z:DV:dZ:tZ"
			":plusPIDmu:minusPIDmu:plusPIDK:minusPIDK"
			":Hcal:Ecal:nVeloClusters")

	# ______________________________________
	def GetTuple(self, chain):

		print(" ----> The following general mask will be applyied to the chain : \n")
		print(
			'-- muon : {}'
			.format(self.filter_mask['daughter_mask'].split('**')))
		print(
			'-- Jpsi : {}'
			.format(self.filter_mask['mother_mask'].split('**')))
		print(
			'-- other : {}'
			.format(self.filter_mask['other'].split('**')))
		print(
			"\n *** You may also want to check \n"
			" *** AnnaTupleFilterJpsiPbPbV2::IsInLuminosityRegion() \n"
			" *** and AnnaTupleFilterJpsiPbPbV2::IsMuonsGhosts() \n"
			" *** where other cuts are also defined \n")

		ntuple = self.CreateTuple()
		okBranch = self.CheckChainBranch(chain)
		if okBranch is False:
			error(' attributes are missing')
			return None

		# counters
		entry_number = 0
		entry_exlude = 0
		tot_entries = chain.GetEntriesFast()
		muon_all = list()

		print(' --- Start running over events ...')
		with ProgressBar(max_value=tot_entries, silent=False) as bar:
			for entry in chain:
				entry_number += 1
				bar.update_amount(entry_number)

				ok_lumi, v_OWNPV, v_ENDVERTEX = self.IsInLuminosityRegion(entry_number, entry)
				if ok_lumi is False:
					info("entry {} does not pass the luminosity cut".format(entry_number))
					entry_exlude += 1
					continue

				ok_muon = self.PassMuonCuts(entry_number, entry)
				if ok_muon is False:
					info("entry {} do not pass muons cut".format(entry_number))
					entry_exlude += 1
					continue

				# Check muon ghost probability
				is_ghost = self.IsMuonsGhosts(entry_number, entry, muon_all)
				if is_ghost is True:
					info("entry {} most likely have ghosts".format(entry_number))
					entry_exlude += 1
					continue

				ok_mother = self.PassMuonCuts(entry_number, entry)
				if ok_mother is False:
					info("entry {} do not pass mother cut".format(entry_number))
					entry_exlude += 1
					continue

				# Prepare Data
				rho = v_OWNPV.Perp()
				v_OWNPV -= v_ENDVERTEX
				dZ = (getattr(entry, self.mother_leaf + '_ENDVERTEX_Z') - getattr(entry, self.mother_leaf + '_OWNPV_Z')) * 1e-3
				tZ = dZ * 3096.916 / (getattr(entry, self.mother_leaf + '_PZ') * TMath.C())

				ntuple.Fill(
					getattr(entry, self.mother_leaf + '_MM'),
					getattr(entry, self.mother_leaf + '_PT'),
					getattr(entry, self.mother_leaf + '_Y'),
					getattr(entry, self.mother_leaf + '_OWNPV_Z'),
					v_OWNPV.Mag(),
					dZ,
					tZ,
					getattr(entry, self.dimuon_leafs[0] + '_PIDmu'),
					getattr(entry, self.dimuon_leafs[1] + '_PIDmu'),
					getattr(entry, self.dimuon_leafs[0] + '_PIDK'),
					getattr(entry, self.dimuon_leafs[1] + '_PIDK'),
					getattr(entry, 'eHcal'),
					getattr(entry, 'eEcal'),
					getattr(entry, 'nVeloClusters'))

		print(
			' --- Done ! Ran over {} events with {:.1f}% removed from cuts !'
			.format(entry_number, float(entry_exlude) / float(entry_number) * 100))
		return ntuple

	# ______________________________________
	def IsInLuminosityRegion(self, entry_number, entry):
		"""
		require mother inside luminous region

		Returns:
			bool -- [description]
		"""
		OWNPV_X = getattr(entry, self.mother_leaf + '_OWNPV_X')
		OWNPV_Y = getattr(entry, self.mother_leaf + '_OWNPV_Y')
		OWNPV_Z = getattr(entry, self.mother_leaf + '_OWNPV_Z')
		ENDVERTEX_X = getattr(entry, self.mother_leaf + '_ENDVERTEX_X')
		ENDVERTEX_Y = getattr(entry, self.mother_leaf + '_ENDVERTEX_Y')
		ENDVERTEX_Z = getattr(entry, self.mother_leaf + '_ENDVERTEX_Z')
		ENDVERTEX_CHI2 = getattr(entry, self.mother_leaf + '_ENDVERTEX_CHI2')
		ENDVERTEX_NDOF = getattr(entry, self.mother_leaf + '_ENDVERTEX_NDOF')

		if OWNPV_Z < -200. or OWNPV_Z > 200.:
			info("OWNPV out of range (|{:.0f}| > 200)".format(OWNPV_Z))
			return False, None, None
		if ENDVERTEX_Z < -200. or ENDVERTEX_Z > 200.:
			info("ENDVERTEX out of range (|{:.0f}| > 200)".format(ENDVERTEX_Z))
			return False, None, None

		# goodness of the dimuon vertex
		if TMath.Prob(ENDVERTEX_CHI2, ENDVERTEX_NDOF) < 0.5 / 100.0:
			info(
				"vertex chi2/ndf too low ({:.3f} < {:.3f})"
				.format(TMath.Prob(ENDVERTEX_CHI2, ENDVERTEX_NDOF), 0.5 / 100.0))
			return False, None, None

		v_OWNPV = TVector3(OWNPV_X, OWNPV_Y, OWNPV_Z)
		v_ENDVERTEX = TVector3(ENDVERTEX_X, ENDVERTEX_Y, ENDVERTEX_Z)

		OWNPV_R = v_OWNPV.Perp()
		ENDVERTEX_R = v_ENDVERTEX.Perp()

		if OWNPV_R < 0.35 or OWNPV_R > 0.95:
			info(
				"OWNPV_R out of range ({:.2f}), current range is 0.35-0.95"
				.format(OWNPV_R))
			return False, None, None
		if ENDVERTEX_R < 0.35 or ENDVERTEX_R > 0.95:
			info(
				"ENDVERTEX_R out of range ({:.2f}), current range is 0.35-0.95"
				.format(ENDVERTEX_R))
			return False, None, None

		return True, v_OWNPV, v_ENDVERTEX

	# ______________________________________
	def IsMuonsGhosts(self, entry_number, entry, all_muons):
		"""
		Check muons angle to see if not ghost particule

		Returns:
			Bool --
		"""

		muP = TLorentzVector()
		muM = TLorentzVector()
		muP.SetPxPyPzE(
			getattr(entry, self.dimuon_leafs[0] + '_PX'),
			getattr(entry, self.dimuon_leafs[0] + '_PY'),
			getattr(entry, self.dimuon_leafs[0] + '_PZ'),
			getattr(entry, self.dimuon_leafs[0] + '_PE'))
		muM.SetPxPyPzE(
			getattr(entry, self.dimuon_leafs[1] + '_PX'),
			getattr(entry, self.dimuon_leafs[1] + '_PY'),
			getattr(entry, self.dimuon_leafs[1] + '_PZ'),
			getattr(entry, self.dimuon_leafs[1] + '_PE'))

		if entry_number == 1:
			all_muons.append([muP, muM])
			return False
		else:

			for cand in all_muons:
				deltaThetaMuM = cand[0].Angle(muP.Vect())
				deltaThetaMuM = cand[1].Angle(muM.Vect())

				if deltaThetaMuM > 0.9999 and deltaThetaMuM > 0.9999:
					return True
		all_muons.append([muP, muM])
		return False

		# ______________________________________
	def PassMuonCuts(self, entry_number, entry):
		"""
		Check muons angle to see if not ghost particule

		Returns:
			Bool
		"""

		for leaf in self.daughter_leafs:
			for cut in self.filter_mask['daughter_mask'].replace(' ', '').split('**'):
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
