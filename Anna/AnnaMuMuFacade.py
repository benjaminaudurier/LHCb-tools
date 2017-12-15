# =============================================================================
#  @class AnnaMuMuFacade
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 
from .AnnaMuMuConfig import AnnaMuMuConfig
from .AnnaMuMuFitter import AnnaMuMuFitter
from .AnnaMuMuSpectra import AnnaMuMuSpectra
from logging import debug as debug
from logging import error as error
from logging import warning as warning
from logging import info as info
from ROOT import TChain, TFile
import copy
import os.path


class AnnaMuMuFacade:
	"""
	The framework is meant to work inside the LHCb framework 
	as it relies evely on OSTAP.
	So, prior to import this module, the user must be sure to be 
	in an Ostap session (lb-run Bender/latest ostap).

	This class takes 3 arguments :
		- tchain : A first TChain object containing the data.
		
		- tchain2 : A second TChain object, not medatory, but usefull 
					in MC studies for instance (To be implemented).

		- configfile : read by AnnaMuMuConfig to configure 
						our object (See AnnaConfig for details)

	As a facade, each functions call a dedicade class inside the framework when 
	running the task (exp: fit, print(diagrams ... ).
	See the classes and functions documentations for more details.
	"""

	# ______________________________________
	def __init__(self, tchain=None, tchain2=None, configfile=""):
		""" cstr """

		print(" ========== Init AnnaMuMuFacade ========== ")

		self._tchain = tchain
		self._tchain2 = tchain2
		self._configfile = AnnaMuMuConfig()
		
		if self._tchain != None and type(self._tchain) != type(TChain()):
			error("{} != a TChain".format(tchain))
			return

		if self._tchain2 != None and type(self._tchain2) != type(TChain()):
			error("{} != a TChain".format(tchain2))
			return


		# Set _configfile 
		info(" Try to read config file ...")
		if self._configfile.ReadFromFile(configfile) is True:
			info(" ---- config file set !")

		else:
			error("Cannot set config file")

		print(" ========================================= ")
	# ______________________________________
	def __str__(self):
		return "I am your father"

	# ______________________________________
	def AdoptSectra(self, spectra, spectrapath):
		"""Add spectra to result file
		
		Arguments:
			spectra {AnnaMuMuSpectra} --
			spectrapath {str} --
		"""

		if type(spectra) is type(AnnaMuMuSpectra):

			o = self.GetResultFile().GetObject(spectrapath, spectra.GetName())

			if (o) is True:
				print("Replacing {}/{}".format(spectrapath, spectra.GetName()))
				self.GetResultFile().Remove("{}/{}".format(spectrapath, spectra.GetName()))

			adoptOK = self.GetResultFile().Adopt(spectrapath, spectra)

			if adoptOK is True:
				print("+++Spectra {} adopted".format(spectra.GetName()))
			
			else:
				print("Could not adopt spectra {}".format(spectra.GetName()))

		else: 
			print("Error creating spectra")

	# ______________________________________
	def DrawMinv(self, particle_name="jpsi"):
		return

	# ______________________________________
	def DrawFitResults(self, particle_name="jpsi"):
		return

	# ______________________________________
	def DrawNofWhat(self, particle_name="jpsi"):
		return
				
	# ______________________________________
	def FitParticle(self, particle_name="JPsi", binning=[], option=""):
		"""Fit invariant mass spectrum
		
		Run over all combination of Centrality/Cut/FitType from the config.
		The fit process is passed to AnnaMuMuFitter class that return an
		AnnaMuMuSpectra stored in a root file accordingly.
		
		Keyword Arguments:
			particle_name {str} -- Help to select the correct FitType 
									(default: {"jpsi"})
			binning {str || list} -- Could be either a str of a lists. 
									See AnnaMuMuFitter constructor for details
			option {str} -- See AnnaMuMuFitter constructor (default: {""}). 
							
		"""

		print(" ================================================================ ")
		print("      	FitParticle {} for binning {}".format(particle_name, binning))
		print(" ================================================================ ")

		print(self._configfile._map)

		for centrality in self._configfile.GetCentrality():
			for cuts in self._configfile.GetCutCombination():
				for leaf in self._configfile.GetLeaf():

					if self._tchain != None:
						spectrapath = "{}/FitParticle/{}/{}/{}".format(
							self._tchain.GetName(),
							centrality,
							cuts,
							leaf
						)
						fitter = AnnaMuMuFitter(particle_name, binning)
						spectra = fitter.Fit(
							self._tchain,
							leaf,
							centrality,
							cuts,
							self._configfile.GetFitType(),
							option
						)
						self.AdoptSectra(spectra, spectrapath)

					if self._tchain2 != None:
						spectrapath = "{}/FitParticle/{}/{}/{}".format(
							self._tchain2.GetName(),
							centrality,
							cuts,
							leaf
						)
						fitter = AnnaMuMuFitter(particle_name, binning)
						spectra = fitter.Fit(
							self._tchain2,
							leaf,
							centrality,
							cuts,
							self._configfile.GetFitType(),
							option
						)
						self.AdoptSectra(spectra, spectrapath)

		return

	# ______________________________________
	def GetResultFile(self):
		""" Create / get results file in the local directory """
		if os.path.isfile('./AnnaResults.root'):
			print('Opening result file ...')
			f = TFile('AnnaResults.root')
			return f

		else:
			print("Creating Result File ...")
			f = TFile.Open('AnnaResults.root', 'recreate')
			return f

	# ______________________________________
	def SaveResults(self, AnnaMuMuResults):
		return

# =============================================================================
# The END 
# =============================================================================
