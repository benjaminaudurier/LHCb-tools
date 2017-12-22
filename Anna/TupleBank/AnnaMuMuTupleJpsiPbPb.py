# =============================================================================
## @class AnnaMuMuTupleBase
#  Mother class of all the sparse
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-12-21 

from logging import error
from .AnnaMuMuTupleBase import AnnaMuMuTupleBase
from ROOT import TNtuple, TVector3, TMath
from Ostap.PyRoUts import *
from logging import info

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
		
		AnnaMuMuTupleBase.__init__(self, mother_leaf, dimuon_leafs, 'AnnaMuMuTupleJpsiPbPb')
		self.filter_mask = {
			"muon_mask": 'PT>750|TRACK_GhostProb<0.5|ProbNNghost<0.8|TRACK_CHI2NDOF<3|IP_OWNPV<3|PIDmu>0|PIDK<6|CosTheta<0.9999',
			"mother_mask": '',
			"other": 'nPVs>0'
		}

		# ______________________________________
	def CheckChainBranch(self, chain):
		"""Make sure the chain has the requiered leafs
		Arguments:
			chain {TChain} -- 
		"""

		# vertex info
		for axis in ['X', 'Y', 'Z']:
			try:
				br = chain.GetBranch(self.mother_leaf + '_OWNPV_' + axis)
			except AttributeError:
				error("AnnaMuMuSparseJpsiPbPb:CheckChainBranch: No info {}_OWNPV_{} leafs in chain".format(self.mother_leaf, axis))
				return False
			try:
				br = chain.GetBranch(self.mother_leaf + '_ENDVERTEX_' + axis)
			except AttributeError:
				error("AnnaMuMuSparseJpsiPbPb:CheckChainBranch: No info {}_ENDVERTEX_{} leafs in chain".format(self.mother_leaf, axis))
				return False

		# mother info
		try:
			br = chain.GetBranch(self.mother_leaf + '_MM')
		except AttributeError:
			error("AnnaMuMuSparseJpsiPbPb:CheckChainBranch: No info {}_MM leafs in chain".format(self.mother_leaf))
			return False
		try:
			br = chain.GetBranch(self.mother_leaf + '_PT')
		except AttributeError:
			error("AnnaMuMuSparseJpsiPbPb:CheckChainBranch: No info {}_MM leafs in chain".format(self.mother_leaf))
			return False
		try:
			br = chain.GetBranch(self.mother_leaf + '_Y')
		except AttributeError:
			error("AnnaMuMuSparseJpsiPbPb:CheckChainBranch: No info {}_MM leafs in chain".format(self.mother_leaf))
			return False

		# dimuon info
		for muon in self.dimuon_leafs:
			try:
				br = chain.GetBranch(muon + '_PIDmu')
			except AttributeError:
				error("AnnaMuMuSparseJpsiPbPb:CheckChainBranch: No info {}_PIDmu leafs in chain".format(muon))
				return False
			try:
				br = chain.GetBranch(muon + '_PIDK')
			except AttributeError:
				error("AnnaMuMuSparseJpsiPbPb:CheckChainBranch: No info {}_PIDK leafs in chain".format(muon))
				return False

		# other
		try:
			br = chain.GetBranch('eHcal')
		except AttributeError:
			error("AnnaMuMuSparseJpsiPbPb:CheckChainBranch: No info eHcal leafs in chain")
			return False
		try:
			br = chain.GetBranch('eEcal')
		except AttributeError:
			error("AnnaMuMuSparseJpsiPbPb:CheckChainBranch: No info eEcal leafs in chain")
			return False
		try:
			br = chain.GetBranch('runNumber')
		except AttributeError:
			error("AnnaMuMuSparseJpsiPbPb:CheckChainBranch: No info runNumber leafs in chain")
			return False

	# ______________________________________
	def CreateTuple(self):
		
		return TNtuple(self.name, self.name, "MM:PT:Y:OWNPV_Z:rho:DV:dZ:tZ:plusPIDmu:minusPIDmu:plusPIDK:minusPIDK:Hcal:Ecal:nVeloClusters")

	# ______________________________________
	def GetTuple(self, chain):

		general_mask = self.GetGeneralMask()
		print(" --- Creating tuple using AnnaMuMuSparseJpsiPbPb class \n")
		print(" -----> The following general mask will be applyied to the chain : \n")
		print(self.filter_mask)

		if general_mask is None:
			error('AnnaMuMuSparseJpsiPbPb::GetTuple: Cannot get the mask')
			return None

		ntuple = self.CreateTuple()
		if self.CheckChainBranch(chain) is False: 
			error('AnnaMuMuSparseJpsiPbPb::CheckChainBranch: attributes are missing')
			return None

		entry_number = 0

		print(' --- Start running over events ...')
		for entry in chain.withCuts(general_mask):
			entry_number += 1
			if entry_number%1000 == 0: print('event {}'.format(entry_number))

			ok_lumi, v_OWNPV, v_ENDVERTEX = self.IsInLuminosityRegion(entry_number, entry)
			if ok_lumi == False:
				info("entry {} does not pass the luminosity cut".format(entry_number))
				continue
			# Prepare Data
			rho = v_OWNPV.Perp()
			v_OWNPV -= v_ENDVERTEX
			# in meters
			dZ = (
				getattr(entry, self.mother_leaf + '_ENDVERTEX_Z') - 
				getattr(entry, self.mother_leaf + '_OWNPV_Z') ) * 1e-3
			tZ = dZ * 3096.916 / (getattr(entry, self.mother_leaf + '_PZ') * TMath.C())

			data = [
				getattr(entry, self.mother_leaf + '_MM'),
				getattr(entry, self.mother_leaf + '_PT'),
				getattr(entry, self.mother_leaf + '_Y'),
				getattr(entry, self.mother_leaf + '_OWNPV_Z'),
				rho,
				v_OWNPV.Mag(),
				dZ,
				tZ,
				getattr(entry, self.dimuon_leafs[0] + '_PIDmu'),
				getattr(entry, self.dimuon_leafs[1] + '_PIDmu'),
				getattr(entry, self.dimuon_leafs[0] + '_PIDK'),
				getattr(entry, self.dimuon_leafs[1] + '_PIDK'),
				getattr(entry, 'eHcal'),
				getattr(entry, 'eEcal'),
				getattr(entry, 'nVeloClusters')]

			ntuple.Fill(
				data[0],
				data[1],
				data[2],
				data[3],
				data[4],
				data[5],
				data[6],
				data[7],
				data[8],
				data[9],
				data[10],
				data[11],
				data[12],
				data[13])
		
		print(' --- Done ! Run over {} events ! Returning tuple ...'.format(entry_number))
		return ntuple

	# ______________________________________
	def IsInLuminosityRegion(self, entry_number, entry):
		""" require mother inside luminous region """
		try:
			OWNPV_X = getattr(entry, self.mother_leaf + '_OWNPV_X')
		except AttributeError:
			error("AnnaMuMuSparseJpsiPbPb:IsInLuminosityRegion: No info OWNPV_X in entry {}".format(entry_number))
			return False, None, None
		try:
			OWNPV_Y = getattr(entry, self.mother_leaf + '_OWNPV_Y')
		except AttributeError:
			error("AnnaMuMuSparseJpsiPbPb:IsInLuminosityRegion: No info OWNPV_Y in entry {}".format(entry_number))
			return False, None, None
		try:
			OWNPV_Z = getattr(entry, self.mother_leaf + '_OWNPV_Z')
		except AttributeError:
			error("AnnaMuMuSparseJpsiPbPb:IsInLuminosityRegion: No info OWNPV_Z in entry {}".format(entry_number))
			return False, None, None
		try:
			ENDVERTEX_X = getattr(entry, self.mother_leaf + '_ENDVERTEX_X')
		except AttributeError:
			error("AnnaMuMuSparseJpsiPbPb:IsInLuminosityRegion: No info ENDVERTEX_X in entry {}".format(entry_number))
			return False, None, None
		try:
			ENDVERTEX_Y = getattr(entry, self.mother_leaf + '_ENDVERTEX_Y')
		except AttributeError:
			error("AnnaMuMuSparseJpsiPbPb:IsInLuminosityRegion: No info ENDVERTEX_Y in entry {}".format(entry_number))
			return False, None, None
		try:
			ENDVERTEX_Z = getattr(entry, self.mother_leaf + '_ENDVERTEX_Z')
		except AttributeError:
			error("AnnaMuMuSparseJpsiPbPb:IsInLuminosityRegion: No info ENDVERTEX_Z in entry {}".format(entry_number))
			return False, None, None

		if OWNPV_Z < -200. or OWNPV_Z > 200.: 
			info("AnnaMuMuSparseJpsiPbPb:IsInLuminosityRegion: OWNPV out of range")
			return False, None, None
		if ENDVERTEX_Z < -200. or ENDVERTEX_Z > 200.:
			info("AnnaMuMuSparseJpsiPbPb:IsInLuminosityRegion: ENDVERTEX out of range")
			return False, None, None

		v_OWNPV = TVector3(OWNPV_X, OWNPV_Y, OWNPV_Z)
		v_ENDVERTEX = TVector3(ENDVERTEX_X, ENDVERTEX_Y, ENDVERTEX_Z)

		OWNPV_R = v_OWNPV.Perp()
		ENDVERTEX_R = v_ENDVERTEX.Perp()

		if OWNPV_R < 0.35 or OWNPV_R > 0.95:
			info("IsInLuminosityRegion: OWNPV_R out of range") 
			return False, None, None
		if ENDVERTEX_R < 0.35 or ENDVERTEX_R > 0.95:
			info("IsInLuminosityRegion: ENDVERTEX_R out of range")
			return False, None, None

		return True, v_OWNPV, v_ENDVERTEX



# =============================================================================
# The END 
# =============================================================================