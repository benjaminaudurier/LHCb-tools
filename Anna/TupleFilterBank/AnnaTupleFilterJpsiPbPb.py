# =============================================================================
#  @class AnnaTupleFilterJpsiPbPb
#  Tuple filter for 2015 PbPb Analysis
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-12-21

from logging import error
from .AnnaTupleFilterBase import AnnaTupleFilterBase
from ROOT import TNtuple, TVector3, TMath, TLorentzVector
from Ostap.PyRoUts import *
from logging import info


# ______________________________________
class AnnaTupleFilterJpsiPbPb(AnnaTupleFilterBase):

	# ______________________________________
	def __init__(self, mother_leaf='', daughter_leafs=['']):
		"""THnSparse for Jpsi PbPb Analysis

		Keyword Arguments:
			mother_leaf {str} -- (default: {''})
			daughter_leafs {list} -- (default: {[''})
			name {str} -- (default: {''})
		"""

		AnnaTupleFilterBase.__init__(self, mother_leaf, daughter_leafs)
		self.name = 'AnnaTupleFilterJpsiPbPb'

		self.filter_mask["dimuon_mask"] = 'TRACK_GhostProb<0.5 '\
			'** ProbNNghost<0.8 ** TRACK_CHI2NDOF<3.'\
			'** IP_OWNPV<3.** PIDmu > 3 ** ETA<4.5 ** ETA>2.0'

		self.filter_mask["mother_mask"] = 'Y<4.5 ** Y>2.0'
		self.filter_mask["other"] = 'nPVs>0'

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
		for muon in self.daughter_leafs:
			for attr in ['_PIDmu', '_CosTheta', '_PIDK', '_ETA']:
				try:
					assert str(muon + attr) in chain.GetListOfBranches()
				except AssertionError:
					error(" No info {}_{} branch in chain".format(muon, attr))
					return False

			for axis in ['X', 'Y', 'Z', 'E']:
				try:
					assert str(muon + '_P' + axis) in chain.GetListOfBranches()
				except AssertionError:
					error(" No info {}_P{} branch in chain".format(muon, axis))
					return False

		# other
		for attr in ['eHcal', 'eEcal', 'runNumber']:
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
			"{0}_MM:{0}_PT:{0}_Y:{0}_Z:{0}_DV:{0}_dZ:{0}_tZ:nVeloClusters:runNumber"
			.format(self.mother_leaf))

	# ______________________________________
	def GetGeneralMask(self):
		"""Return the general cut masks
		to be applied before running over
		Chain events

		Returns:
			[str] -- [description]
		"""

		if self.filter_mask is None:
			error(" no filter mask !")
			return None

		# Get masks
		general_mask = ''
		if self.filter_mask['dimuon_mask'] != '':
			for leaf in self.daughter_leafs:
				for cut in self.filter_mask['dimuon_mask'].split('**'):
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
		"""The main method of the class

		Here the class run in all events in the tree/chain
		and return a filled new tuple for events passing the
		selection

		Arguments:
			chain {TChain}

		Returns:
			TNtuple
		"""

		general_mask = self.GetGeneralMask()
		print(" ----> The following general mask will be applyied to the chain : \n")
		print(
			'-- muon : {}'
			.format(self.filter_mask['dimuon_mask'].split('**')))
		print(
			'-- Jpsi : {}'
			.format(self.filter_mask['mother_mask'].split('**')))
		print(
			'-- other : {}'
			.format(self.filter_mask['other'].split('**')))
		print(
			"\n *** You may also want to check \n"
			" *** AnnaTupleFilterJpsiPbPb::IsInLuminosityRegion() \n"
			" *** and AnnaTupleFilterJpsiPbPb::IsMuonsGhosts() \n"
			" *** where other cuts are also defined \n")

		if general_mask is None:
			error(':GetTuple: Cannot get the mask')
			return None

		ntuple = self.CreateTuple()
		okBranch = self.CheckChainBranch(chain)
		if okBranch is False:
			error(' attributes are missing')
			return None

		# counters
		entry_number = 0
		entry_exlude = 0
		muon_all = list()

		print(' --- Start running over events ...')
		for entry in chain.withCuts(general_mask, progress=True):
			entry_number += 1

			# Check the vertex position
			ok_lumi, v_OWNPV, v_ENDVERTEX = self.IsInLuminosityRegion(entry_number, entry)
			if ok_lumi is False:
				info("entry {} does not pass the luminosity cut".format(entry_number))
				entry_exlude += 1
				continue

			# Check muon ghost probability
			is_ghost = self.IsMuonsGhosts(entry_number, entry, muon_all)
			if is_ghost is True:
				info("entry {} most likely have ghosts".format(entry_number))
				entry_exlude += 1
				continue

			# Prepare Data
			v_OWNPV -= v_ENDVERTEX
			dZ = (
				getattr(entry, self.mother_leaf + '_ENDVERTEX_Z') -
				getattr(entry, self.mother_leaf + '_OWNPV_Z')) * 1e-3
			tZ = dZ * 3096.916 / (getattr(entry, self.mother_leaf + '_PZ') * TMath.C())

			ntuple.Fill(
				getattr(entry, self.mother_leaf + '_MM'),
				getattr(entry, self.mother_leaf + '_PT'),
				getattr(entry, self.mother_leaf + '_Y'),
				getattr(entry, self.mother_leaf + '_OWNPV_Z'),
				v_OWNPV.Mag(),
				dZ,
				tZ,
				getattr(entry, 'nVeloClusters'),
				getattr(entry, 'runNumber'),)

		print(
			' --- Done ! Ran over {} events with {:.1f}% removed from cuts !'
			.format(entry_number, float(entry_exlude) / float(entry_number) * 100))
		return ntuple

	# ______________________________________
	def IsInLuminosityRegion(self, entry_number, entry):
		"""
		require mother inside luminous region

		Returns:
			bool
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
	def IsMuonsGhosts(self, entry_number, entry, prev_muons):
		"""
		Check if muon angls between current candidate
		and previous one are not too close

		Returns:
			Bool
		"""

		mu1 = TLorentzVector()
		mu2 = TLorentzVector()
		mu1.SetPxPyPzE(
			getattr(entry, self.daughter_leafs[0] + '_PX'),
			getattr(entry, self.daughter_leafs[0] + '_PY'),
			getattr(entry, self.daughter_leafs[0] + '_PZ'),
			getattr(entry, self.daughter_leafs[0] + '_PE'))
		mu2.SetPxPyPzE(
			getattr(entry, self.daughter_leafs[1] + '_PX'),
			getattr(entry, self.daughter_leafs[1] + '_PY'),
			getattr(entry, self.daughter_leafs[1] + '_PZ'),
			getattr(entry, self.daughter_leafs[1] + '_PE'))

		if entry_number == 1:
			prev_muons.append(mu1)
			prev_muons.append(mu2)
			return False
		else:

			deltaThetaMu1 = prev_muons[0].Angle(mu1.Vect())
			deltaThetaMu2 = prev_muons[1].Angle(mu2.Vect())

			if deltaThetaMu1 > 0.9999 and deltaThetaMu2 > 0.9999:
				prev_muons[0] = mu1
				prev_muons[1] = mu2
				return True

		prev_muons[0] = mu1
		prev_muons[1] = mu2
		return False

# =============================================================================
# The END
# =============================================================================
