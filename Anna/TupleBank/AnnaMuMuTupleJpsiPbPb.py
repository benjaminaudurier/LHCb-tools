# =============================================================================
## @class AnnaMuMuTupleBase
#  Mother class of all the sparse
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-12-21

from logging import error
from .AnnaMuMuTupleBase import AnnaMuMuTupleBase
from ROOT import TNtuple, TVector3, TMath
from Ostap.PyRoUts import *
from logging import info, warning

# ______________________________________
class AnnaMuMuTupleJpsiPbPb(AnnaMuMuTupleBase):

	# ______________________________________
	def __init__(self, mother_leaf='', dimuon_leafs=['', '']):
		"""THnSparse for Jpsi PbPb Analysis

		Keyword Arguments:
			mother_leaf {str} -- (default: {''})
			dimuon_leafs {list} -- (default: {[''})
			name {str} -- (default: {''})
		"""

		AnnaMuMuTupleBase.__init__(
			self,
			mother_leaf,
			dimuon_leafs,
			'AnnaMuMuTupleJpsiPbPb')

		self.filter_mask = {
			"muon_mask": 'PT>750. ** TRACK_GhostProb<0.5 ** ProbNNghost<0.8 ** TRACK_CHI2NDOF<3. ** IP_OWNPV<3. ** PIDmu>3 ** PIDK  < 6.',
			"mother_mask": '',
			"other": 'nPVs>0 ** nVeloTracks >0'}

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
		for attr in ['_MM', '_PT', '_Y', '_Hlt1BBMicroBiasVeloDecision_Dec']:
			try:
				assert str(self.mother_leaf + attr) in chain.GetListOfBranches()
			except AssertionError:
				error(" No info {}_{} branch in chain".format(self.mother_leaf, attr))
				return False

		# dimuon info
		for muon in self.dimuon_leafs:
			for attr in ['_PIDmu', '_CosTheta', '_PIDK']:
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
			"MM:PT:Y:OWNPV_Z:rho:DV:dZ:tZ:eHcal:eEcal:nVeloClusters:runNumber:Hlt1BBMicroBiasVeloDecision")

	# ______________________________________
	def GetTuple(self, chain):

		general_mask = self.GetGeneralMask()
		print(" ----> The following general mask will be applyied to the chain : \n")
		print(
			'-- muon_mask : {}'
			.format(self.filter_mask['muon_mask'].split('**')))
		print(
			'-- mother_mask : {}'
			.format(self.filter_mask['mother_mask'].split('**')))
		print(
			'-- other : {}'
			.format(self.filter_mask['other'].split('**')))
		print(
			"\n *** You may also want to check \n"
			" *** AnnaMuMuTupleJpsiPbPb::IsInLuminosityRegion() \n"
			" *** and AnnaMuMuTupleJpsiPbPb::IsMuonsGhosts() \n"
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

		print(' --- Start running over events ...')
		for entry in chain.withCuts(general_mask, progress=True):
			entry_number += 1
			# if entry_number % 100 == 0:
			# 	print('- event {}'.format(entry_number))

			ok_lumi, v_OWNPV, v_ENDVERTEX = self.IsInLuminosityRegion(entry_number, entry)
			if ok_lumi is False:
				info("entry {} does not pass the luminosity cut".format(entry_number))
				entry_exlude += 1
				continue

			ok_ghost = self.IsMuonsGhosts(entry_number, entry)
			if ok_ghost is False:
				info("entry {} most likely have ghosts".format(entry_number))
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
				rho,
				v_OWNPV.Mag(),
				dZ,
				tZ,
				getattr(entry, 'eHcal'),
				getattr(entry, 'eEcal'),
				getattr(entry, 'nVeloClusters'),
				getattr(entry, 'runNumber',
				getattr(entry, self.mother_leaf + '_Hlt1BBMicroBiasVeloDecision_Dec')))

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
		try:
			OWNPV_X = getattr(entry, self.mother_leaf + '_OWNPV_X')
		except AttributeError:
			warning("No info {}_OWNPV_X in entry {}".format(self.mother_leaf, entry_number))
			return False, None, None
		try:
			OWNPV_Y = getattr(entry, self.mother_leaf + '_OWNPV_Y')
		except AttributeError:
			warning("No info {}_OWNPV_Y in entry {}".format(self.mother_leaf, entry_number))
			return False, None, None
		try:
			OWNPV_Z = getattr(entry, self.mother_leaf + '_OWNPV_Z')
		except AttributeError:
			warning("No info {}_OWNPV_Z in entry {}".format(self.mother_leaf, entry_number))
			return False, None, None
		try:
			ENDVERTEX_X = getattr(entry, self.mother_leaf + '_ENDVERTEX_X')
		except AttributeError:
			warning("No info {}_ENDVERTEX_X in entry {}".format(self.mother_leaf, entry_number))
			return False, None, None
		try:
			ENDVERTEX_Y = getattr(entry, self.mother_leaf + '_ENDVERTEX_Y')
		except AttributeError:
			warning("No info {}_ENDVERTEX_Y in entry {}".format(self.mother_leaf, entry_number))
			return False, None, None
		try:
			ENDVERTEX_Z = getattr(entry, self.mother_leaf + '_ENDVERTEX_Z')
		except AttributeError:
			warning("No info {}_ENDVERTEX_Z in entry {}".format(self.mother_leaf, entry_number))
			return False, None, None
		try:
			ENDVERTEX_CHI2 = getattr(entry, self.mother_leaf + '_ENDVERTEX_CHI2')
		except AttributeError:
			warning("No info {}_ENDVERTEX_CHI2 in entry {}".format(self.mother_leaf, entry_number))
			return False, None, None
		try:
			ENDVERTEX_NDOF = getattr(entry, self.mother_leaf + '_ENDVERTEX_NDOF')
		except AttributeError:
			warning("No info {}_ENDVERTEX_NDOF in entry {}".format(self.mother_leaf, entry_number))
			return False, None, None

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
	def IsMuonsGhosts(self, entry_number, entry):
		"""
		Check muons angle to see if not ghost particule

		Returns:
			Bool --
		"""

		try:
			costheta_mu1 = getattr(entry, self.dimuon_leafs[0] + '_CosTheta')
		except AttributeError:
			warning(
				"No info {}_CosTheta in entry {}"
				.format(self.dimuon_leafs[0], entry_number))
			return False
		try:
			costheta_mu2 = getattr(entry, self.dimuon_leafs[1] + '_CosTheta')
		except AttributeError:
			warning(
				"No info {}_CosTheta in entry {}"
				.format(self.dimuon_leafs[1], entry_number))
			return False

		if costheta_mu1 > 0.9999 and costheta_mu2 > 0.9999:
			return False
		else:
			return True

# =============================================================================
# The END
# =============================================================================
