# =============================================================================
#  @class AnnaMuMuFitter
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 

from .AnnaMuMuSpectra import AnnaMuMuSpectra
from .AnnaMuMuResult import AnnaMuMuResult
import ROOT
# OSTAP modules
from Ostap.PyRoUts import *
import Ostap.FitModels as Models
# Python modules
from logging import debug, error, warning, info


class AnnaMuMuFitter:
	"""helper class for fit process.
	
	This class comes with default binnings that can be set
	differently according to binning 
	"""
	# ______________________________________
	def __init__(self, particle=None, binning=[]):
		"""cstr
				
		Keyword Arguments:
			particle {str} -- use for setting purposes (default: {""})
			binning {list} -- the binning (or leaf name on which we apply cut). 
					By convention, binning[0] should contain the name of the binning.
					exemple:
						["JPSI_PT", 0., 4000., 8000.]
					Could also be 2D :
						[["JPSI_PT", 0., 4000., 8000.], ["JPSI_P", 0., 4000., 8000.] ]
		"""
				
		# Centrality percentage based on VELO cluster cut
		self._centrality = {
			"branch": ["VELOTHITS"], 
			"90_100": [0, 1311],
			"80_90": [1311, 3009],
			"70_80": [3009, 5580],
			"60_70": [5580, 9685],
			"50_60": [9685, 15417],
			"40_50": [15417, 22473]
		}

		# Adopt binning
		self._binning, self._2D = self.CheckBinning(binning)
		if not self._binning:
			print("Binning is not good ...")
			return None

		# Several dictionnaries used for fit
		# WHATCH OUT WHEN TOUCHING THIS !
		self._fit_key = {
			"signal": "",
			"bckgr": "",
			"weight": None
		}

		# Mass map
		self._mass_map = {
			"JPsi": ROOT.RooRealVar(
				'JPsi_mass', 'J/psi(1S) mass', 3000., 3300.),
			"PsiP": ROOT.RooRealVar(
				'PsiP_mass', 'Psi(2S) mass', 3600., 3800.),
			"Upsilon": ROOT.RooRealVar(
				'Upsilon_mass', 'Upsilon (1S) mass', 8500., 10500.),
			"UpsilonPrime": ROOT.RooRealVar(
				'UpsilonPrime_mass', 'Upsilon (2S) mass', 9000., 11000.)
		}

		# Set particule name
		try:
			assert particle in self._mass_map.keys()
		except AssertionError:
			error('''Wrong entry for particle ({}),
				possibles are {}'''.self._mass_map.keys())
			return None
		self._particle_name = particle 
		
	# ______________________________________
	def CheckBinning(self, binning):
		"""Check binning format
		
		Fiew tests to check if binning pass several conditions
		
		Arguments:
			binning {list}
		
		Returns:
			bool -- Binning pass the conditions or not
		"""

		ok = True
		is2D = False
		
		# Check size
		try:
			assert len(binning) > 2
		except AssertionError:
			print("binning is too small")
			ok = False

		# Check if 2D binning
		if type(binning[0]) == list():
			try:
				assert type(binning[1]) == list()
			except AssertionError:
				error(
					" --- Wrong bin format ({}),\
					should be list()".format(type(binning[1]))
				)
				return False

			print(' --- Fit with a 2D binning {}-{}'.format)
			(
				binning[0][0],
				binning[1][0]
			)
			is2D = True

		# Further checks for 1D binning
		if is2D is False:
			# Check binning size
			try:
				assert len(binning[1:]) > 2
			except AssertionError:
				error("Not enought bins ({}),\
				required at least 2".format(len(binning[1:])))
				ok = False

			# Check binning ordening
			if ok is True:
				for i, limit in enumerate(binning[1:-1]):
					try:
						assert limit < binning[i + 2] 
					except AssertionError:
						error(" Binning {} not order properly".format())
						ok = False

		else:
			# Check binning size
			try:
				assert len(binning[0][1:]) > 2
			except AssertionError:
				error("Not enought bins ({}), \
				required at least 2".format(len(binning[0][1:])))
				ok = False
			try:
				assert len(binning[1][1:]) > 2
			except AssertionError:
				error("Not enought bins ({}), \
				required at least 2".format(len(binning[1][1:])))
				ok = False

			# Check binning ordening
			if ok is True:
				for i, limit in enumerate(binning[0][1:-1]):
					try:
						assert limit < binning[0][i + 2]
					except AssertionError:
						error(" Binning {} not order properly".format())
						ok = False
				for i, limit in enumerate(binning[1][1:-1]):
					try:
						assert limit < binning[1][i + 2]
					except AssertionError:
						error(" Binning {} not order properly".format())
						ok = False

		try:
			assert ok is True
		except AssertionError:
			error("Binning is wrong")
			return None, None

		debug("Binning is correct")
		return binning, is2D

	# ______________________________________
	def ConfigureCuts(self, centrality, cut, bintype, bin_limits):

		cut_update = str()		

		if self._2D is True:
			bin_names = bintype.split('--')
			cut_update = "{2} < {0} && {0} < {3} && {4} < {1} && {1} < {5}".format(
				bin_names[0],
				bin_names[1],
				bin_limits[0],
				bin_limits[1],
				bin_limits[2],
				bin_limits[3]
			) 
		else:
			cut_update = "{1} < {0} && {0} < {2}".format(
				bintype,
				bin_limits[0],
				bin_limits[1]
			)

		add_centrality = True
		try:
			self._centrality[centrality]
		except KeyError:
			add_centrality = False
			warning("ConfigureCuts: skip centrality cut ({})".format(centrality))

		add_cut = True
		try:
			assert cut != "#"
		except AssertionError:
			warning("ConfigureCuts: skip specific cut ({})".format(centrality))
			add_cut = False

		if add_centrality is True:
			cut_update += " && {0}>{1} && {0}<{2}".format(
				self._centrality["branch"],
				self._centrality[centrality][0],
				self._centrality[centrality][1]
			) 
		if add_cut is True:
			cut_update += " && {0}".format(cut) 
		return cut_update

	# ______________________________________
	def DecodeFitType(self, fit_type):
		"""Decode the string containing all 
			the information for the fit to be performed.
		
		The fit_type must be combination of key=value pairs separated by "|".
		Default keys are available in self._key_value

		Appart from the [signal] and [bckgr] keys, others have default values.
		If the key is different from standard key value it is assumed
		to be the value for a parameter of the fit function.
				
		Arguments:
			fit_type {str} -- example : 
				particle=JPsi|leaf=jpsi_M|range=2;5|signal=CB2_pdf|bckgr=Bkg_pdf
		
		Returns:
			bool -- If the fit is correctly decoded 
		"""

		# Always reset the data member at each fit_type
		self._fit_key["weight"] = 1

		if fit_type.count("signal") != 1 or fit_type.count("bckgr") != 1:
			error(
				"""DecodeFitType: Cannot decode type. 
				Expecting 1 entries with 'signal' and 'bckgr, found {} and {}"""
				.format(
					fit_type.count("signal"),
					fit_type.count("bckgr")))
			return False

		# Check that keys appear only once in the string
		for x in self._fit_key.keys():
			try:
				assert fit_type.count(x) < 2 
			except AssertionError:
				error(" Oups ! Multiple entries for {}, please fix it !".format(x))
				return False

		# Fill self._fit_key and self._fit_attribute
		pairs = fit_type.split("|")
		for pair in pairs:
			key, value = self.GetKeyValue(pair, '=')

			try:
				assert key != None or value != None
			except AssertionError:
				print('Error : Invalid key=value pair ' + pair)
			debug("key = %s, value = %s".format(key, value))

			self._fit_key[key] = value
		
		return True

	# ______________________________________
	def Fit(self, tchain, leaf, centrality, cut, fit_types, option):
		"""The main fit method
		
		Histogrames are retrieved according to the cut we apply 
		(all combinations of centrality/cut/self._binning).

		Each histos is fitted for all fit_types and stored in an
		AnnaMuMuResult class ( referred as subresults in the code).

		All subresults for a given binning are stored again in a 
		AnnaMuMuResult class ( referred as result in the code).

		Finally, all results are stored in an AnnaMuMuSpectra class
		that is returned at the end of the method.	

		Arguments:
			tchain {TChain} 
			leaf {str} 
			centrality {str} 
			cut {str} 
			fit_types {list} 
			option {str} 
		
		Returns:
			AnnaMuMuSpectra -- storage class for a results
		"""

		# The spectra that will be return
		spectra = AnnaMuMuSpectra(
			name=self._particle_name + "_" + self.GetBinType(),
			title=self._particle_name + "_" + self.GetBinType())

		# Get list of histograms (one per cut)
		print(' --- try to get histos ...')
		histos = self.GetHistos(tchain, leaf, centrality, cut)
		print(' --- histos retrived ...')
		debug("Fit: histos = {}".format(histos))

		# Construct our AnnaMuMuRestult for each histo or bins
		annaresults = [
			AnnaMuMuResult(self.GetBinType(), self.GetBinsAsString()[i]) 
			for i in range(0, len(histos))
		]

		# Run over each AnnaResults (or bin or histos) and add subresults
		added_result = 0
		for i, annaresult in enumerate(annaresults):
			debug("Fit: annaresult = {}".format(annaresult))
			subresults = list()
			added_subresult = 0

			# Create a subresults for each fit_type
			subresults.append(self.FitHisto(fit_types, histos[i]))

			# Adopt each subresults
			for subresult in subresults:
				debug("Fit: subresult = {}".format(subresult))
				added_subresult += annaresult.AdoptSubResult(subresult)
				print(
					' ----- number of subresults fitted for {} - {} : {}'
					.format(annaresult.GetName(), self.GetBinsAsString()[i], added_subresult)
				)
			# Finally add result to spectra
			added_result += spectra.AdoptResult(annaresult, self.GetBinsAsString()[i])
				
		print(
			"""number of results added for {} : {}"""
			.format(spectra.GetName(), added_result))

		return spectra

	# ______________________________________
	def FitHisto(self, fit_methods, histo):
		"""Fit Histogram for all fit_methods.
		
		The result is stored in a AnnaMuMuResult
		
		Arguments:
			fit_methods {list} -- fit configuration string
			histo {TH1} -- histo to be fitted
		
		Returns:
			list -- contains all the AnnaMuMuResults
		"""

		try:
			assert histo != None
		except AssertionError:
			error("Cannot get histo")
			return None

		subresult_list = list()
		print(""" \n========= > Fit histo {} < ========= """.format(histo.GetName()))

		for i, fit_method in enumerate(fit_methods):
			# Get the fit configuration
			self.DecodeFitType(fit_method)

			# try to get the fit functions from Ostap
			try:
				getattr(Models, self._fit_key['signal'])
			except AttributeError:
				error('''FitHisto: Cannot find {} in Ostap.FitModels
					for signal function'''.format(self._fit_key['signal']))
				continue
			try:
				background = getattr(Models, self._fit_key['bckgr'])
			except AttributeError:
				error('''FitHisto :Cannot find {} in Ostap.FitModels
					for background function'''.format(self._fit_key['bckgr']))
				continue

			# Configure functions
			signal = getattr(Models, self._fit_key['signal'])(
				'sig',
				self._mass_map[self._particle_name].getMin(),
				self._mass_map[self._particle_name].getMax(),
				mass=self._mass_map[self._particle_name])

			background = getattr(Models, self._fit_key['bckgr'])(
				'bckgr',
				self._mass_map[self._particle_name])
		
			model = Models.Fit1D(signal=signal, background=background)
			self.SetAdditionalAttributeToModelFunction(model)

			print(""" \n------- > with {} + {} (weight = {} ) \n""".format(
				self._fit_key['signal'], self._fit_key['bckgr'],  self._fit_key['weight']))
			result, frame = model.fitTo(histo, silent=True, draw=False, refit=True)
			debug("{}".format(result))

			# Create the AnnaMuMuResult
			sr_name = "{}_{}".format(fit_method, histo.GetName())
			sr = AnnaMuMuResult(name=sr_name, title=histo.GetTitle(), histo=histo)
			sr.weigth = self._fit_key['weight']
			sr.frame = frame
			for key in result.parameters().keys():
				sr.Set(key, result(key)[0], result(key)[1])
			sr.Set("FitResult", result.status(), 0., 0.)
			sr.Set("CovMatrixStatus", result.covQual(), 0., 0.)

			subresult_list.append(sr)

		return subresult_list

	# ______________________________________
	def GetBinType(self):
		
		if self._2D: 
			return self._binning[0][0] + '--' + self._binning[1][0]
		else:
			return self._binning[0]

	# ______________________________________
	def GetBinsAsList(self):

		if self._2D is True:
			return [ 
				[
					self._binning[0][i], self._binning[0][i + 1], 
					self._binning[1][j], self._binning[1][j + 1]
				] 
				for i in range(1, len(self._binning[0][1:]))
				for j in range(1, len(self._binning[1][1:]))
			]
		else:
			return [
				[
					self._binning[i], self._binning[i + 1]
				] 
				for i in range(1, len(self._binning[1:]))
			]

	# ______________________________________
	def GetBinsAsString(self):

		if self._2D is True:
			return [ 	
				"{}_{}_{}_{}".format(
					self._binning[0][i], self._binning[0][i + 1], 
					self._binning[1][j], self._binning[1][j + 1]
				) 
				for i in range(1, len(self._binning[0][1:]))
				for j in range(1, len(self._binning[1][1:]))
			]
		else:
			return [
				"{}_{}".format(
					self._binning[i], self._binning[i + 1]
				)
				for i in range(1, len(self._binning[1:]))
			]

	# ______________________________________
	def GetHistos(self, tchain, leaf, centrality, cut):
		"""Retrieve list of histograms
		
		All histograms are projected from the TChain
		according to each combination of centrality/cut/leaf/binning.
		
		Arguments:
			tchain {TChain} -- 
			leaf {str} -- 
			centrality {str} -- 
			cut {str} -- 
		
		Returns:
			list -- contains al histograms
		"""

		histo_list = list()
		bin_all = self.GetBinsAsList()
		bintype = self.GetBinType() 

		# Check if leaf exist
		try:
			assert tchain.GetLeaf(leaf) != None
		except AssertionError:
			error("GetHistos: cannot find leaf {}".format(leaf))
			return None

		# This is just sweet :)
		histo_cuts = [ 
			self.ConfigureCuts(centrality, cut, bintype, bin_limits)
			for bin_limits in bin_all
		]
		debug("GetHistos: histo_cuts : {}".format(histo_cuts))

		for i, histo_cut in enumerate(histo_cuts):
			print(' --- Getting histo from leaf {} with cut {}'.format(leaf, histo_cut))
			command = '{}>>histo'.format(leaf)
			tchain.Draw(command, histo_cut, "goff")

			try:
				assert ROOT.gDirectory.Get("histo") != None
			except AssertionError:
				error("GetHistos: cannot get histo from leaf {} ... continue".format(leaf))
				continue

			try:
				histo_list.append(ROOT.gDirectory.Get("histo").Clone())
			except ReferenceError:
				error("GetHistos: could not get histo with cut {}".format(histo_cut))
				continue

			histo_list[i].SetName("{}_{}".format(leaf, bin_all[i])) 

		return histo_list

	# ______________________________________
	def GetKeyValue(self, pair, separator):

		if pair.count(separator) != 1:
			return None, None

		split_pair = pair.strip()
		split_pair = split_pair.split(separator)
		return split_pair[0], split_pair[1]

	# ______________________________________
	def SetAdditionalAttributeToModelFunction(self, model):
		"""Run over self._fit_key and try to configure
		fit model if possible
				
		Arguments:
			model {Ostap.FitModels} -- 
		"""

		# First check we have arguments
		attributes_set = list()

		# Check if attribute belong to the signal part and set it if true
		for i, attribute in enumerate(self._fit_key.keys()):
			try:
				getattr(model.signal, attribute)
			except AttributeError:
				debug(
					'''No {} in the signal part of the model'''
					.format(attribute))
				continue
			setattr(model.signal, attribute, self._fit_key[attribute])
			attributes_set.append('signal.'+attribute)

		# Check if attribute belong to the background part and set it if true
		for attribute in self._fit_key.keys():
			try:
				getattr(model.background, attribute)
			except AttributeError:
				debug(
					'''No {} in the background part of the model'''
					.format(attribute))
				continue
			setattr(model.background, attribute, self._fit_key[attribute])
			attributes_set.append('background.'+attribute)

		# Check if attribute belong to the model itself and set it if true
		for attribute in self._fit_key.keys():
			try:
				getattr(model, attribute)
			except AttributeError:
				debug(
					'''No {} in the background part of the model'''
					.format(attribute))
				continue
			setattr(model, attribute, self._fit_key[attribute])
			attributes_set.append('model.'+attribute)

		debug(
			"SetAdditionalAttributeToModelFunction: Additionnal Attributes sets : {}"
			.format(attributes_set))


# =============================================================================
# The END 
# =============================================================================