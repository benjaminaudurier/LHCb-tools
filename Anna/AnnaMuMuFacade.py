# =============================================================================
#  @class AnnaMuMuFacade
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 
from .AnnaMuMuConfig import AnnaMuMuConfig
from .AnnaMuMuFitter import AnnaMuMuFitter
from logging import debug, error, info
from ROOT import TChain, TFile
import Ostap.ZipShelve as DBASE
import os.path


class AnnaMuMuFacade:
	"""
	The framework is meant to work inside the LHCb framework 
	as it relies on OSTAP for the fits and the saving data.
	So, prior to import this module, the user must be sure to be 
	in an Ostap session (lb-run Bender/latest ostap).

	This class takes 3 arguments :
		- tchain : A first TChain object containing the data.
		
		- tchain2 : A second TChain object, not medatory, but usefull 
					in MC studies for instance (just in case in the futur).

		- configfile : read by AnnaMuMuConfig to configure 
						our object (See AnnaConfig for details)

	As a facade, each functions call a dedicade class inside the framework who 
	actually makes the job (exp: fit, print(diagrams ... ).
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
			error("{} is not a TChain".format(tchain))
			return

		if self._tchain2 != None and type(self._tchain2) != type(TChain()):
			error("{} is not a TChain".format(tchain2))
			return

		# Set _configfile 
		info(" Try to read config file ...")
		if self._configfile.ReadFromFile(configfile) is True:
			info(" ---- config file set !")

		else:
			error("Cannot set config file")

		print(" ========================================= \n\n")
	# ______________________________________
	def __str__(self):
		return "I am your father"

	# ______________________________________
	def AdoptResult(self, result, result_path):
		"""Add result to RootShelve file result.
		
		The method create / get a RootShelve file in the local directory
		called AnnaResults.
		
		Arguments:
			result {[type]} -- must inherit from TObject
			result_path {[type]} -- path inside AnnaResults.root
		"""

		# Create / get results file in the local directory """
		
		db = DBASE.open('AnnaMuMu')

		if db != None:
			debug('AdoptResult: result : {}'.format(result))

			# Check if file exists
			try:
				o = db[str(result_path)]
			except KeyError:
				print("No object in {}/{}".format(result_path, result.GetName()))
				o = None

			if o != None:
				print("Replacing {}/{}".format(result_path, result.GetName()))
				del o


			db[str(result_path)] = result 
			if db[str(result_path)] != None:
				print("+++result {} adopted".format(result.GetName()))
			
			else:
				error("AdoptResult: Could not adopt result {}".format(result.GetName()))
				return

		else: 
			error("AdoptResult: Error creating result file")
			return

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
		"""Main Fit method
		
		Run over all combination of Centrality/Cut/Leaf from the config.
		The fit process is passed to AnnaMuMuFitter class that return an
		AnnaMuMuSpectra to be stored in the result TFile.
						
		Keyword Arguments:
			particle_name {str} -- To set the particle mass 
				in AnnaMuMuFitter (default: {"JPsi"})
			binning {list} -- Binning conditions for the fit. (default: {[]})
				Should be a list as [str(leaf_name), x.x, x.x, x.x ...]
				example :
					["JPSI_PT", 0., 4000., 8000.]) 
			option {str} -- possible options (for futur dvlp) (default: {""})
		"""

		print(" ================================================================ ")
		print("      	FitParticle {} for binning {}".format(particle_name, binning))
		print(" ================================================================ ")

		debug("FitParticle: AnnaMuMuConfig map : \n {}".format(self._configfile._map))

		for centrality in self._configfile.GetCentrality():
			for cut in self._configfile.GetCutCombination():
				for leaf in self._configfile.GetLeaf():

					if self._tchain != None:
						spectrapath = "{}/FitParticle/{}/{}/{}".format(
							self._tchain.GetName(),
							centrality,
							cut,
							leaf
						)
						fitter = AnnaMuMuFitter(particle_name, binning)
						spectra = fitter.Fit(
							self._tchain,
							leaf,
							centrality,
							cut,
							self._configfile.GetFitType(),
							option
						)
						self.AdoptResult(spectra, spectrapath)

					if self._tchain2 != None:
						spectrapath = "{}/FitParticle/{}/{}/{}".format(
							self._tchain2.GetName(),
							centrality,
							cut,
							leaf
						)
						fitter = AnnaMuMuFitter(particle_name, binning)
						spectra = fitter.Fit(
							self._tchain2,
							leaf,
							centrality,
							cut,
							self._configfile.GetFitType(),
							option
						)
						self.AdoptResult(spectra, spectrapath)

		return

	# ______________________________________
	def GetResultFile(self):
		""" Create / get results file in the local directory """
		if os.path.isfile('./AnnaResults.root'):
			f = TFile.Open('AnnaResults.root', 'update')
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
