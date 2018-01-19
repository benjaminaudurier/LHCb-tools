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
import inspect


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
			"branch": "nVeloClusters",
			"90_100": [1311, 0],
			"80_90": [3009, 1311],
			"70_80": [5580, 3009],
			"60_70": [9685, 5580],
			"50_60": [15417, 9685],
			"40_50": [22473, 15417],
			"60_90": [9685, 1311],
			"70_90": [5580, 1311]}

		# Adopt binning
		self._binning, self._2D = self.CheckBinning(binning)
		if not self._binning:
			print("Binning is not good ...")
			return None

		# Several dictionnaries used for fit
		self._fit_key = {
			"signal": "",
			"bkgr": "",
			"weight": None}

		# Mass map
		self._mean_map = {
			"JPsi": ROOT.RooRealVar(
				'JPsi_mean', 'J/psi(1S) mean', 3000., 3200.),
			"PsiP": ROOT.RooRealVar(
				'PsiP_mean', 'Psi(2S) mean', 3600., 3800.),
			"Upsilon": ROOT.RooRealVar(
				'Upsilon_mean', 'Upsilon (1S) mean', 8500., 10500.),
			"UpsilonPrime": ROOT.RooRealVar(
				'UpsilonPrime_mean', 'Upsilon (2S) mean', 9000., 11000.)}

		# width map
		self._width_map = {
			"JPsi": ROOT.RooRealVar(
				'JPsi_width', 'J/psi(1S) width', 5., 100.)}

		# Set particule name
		try:
			assert particle in self._mean_map.keys()
		except AssertionError:
			error('''Wrong entry for particle ({}),
				possibles are {}'''.self._mean_map.keys())
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
			assert len(binning) >= 2
		except AssertionError:
			error("binning is too small")
			ok = False

		# Check if 2D binning
		if type(binning[0]) == list():
			try:
				assert type(binning[1]) == list()
			except AssertionError:
				error(
					""" --- Wrong bin format ({}),
					should be list()""".format(type(binning[1]))
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
				assert len(binning[1:]) >= 2
			except AssertionError:
				error(""" Not enought bins ({}),
				required at least 2 """.format(len(binning[1:])))
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
				assert len(binning[0][1:]) >= 2
			except AssertionError:
				error(""" Not enought bins ({}),
				required at least 2 """.format(len(binning[0][1:])))
				ok = False
			try:
				assert len(binning[1][1:]) >= 2
			except AssertionError:
				error("""Not enought bins ({}),
				required at least 2""".format(len(binning[1][1:])))
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
				bin_names[0], bin_names[1],
				bin_limits[0], bin_limits[1], bin_limits[2], bin_limits[3])
		else:
			cut_update = "{1} < {0} && {0} < {2}".format(
				bintype, bin_limits[0], bin_limits[1])

		add_centrality = True
		try:
			self._centrality[centrality]
		except KeyError:
			add_centrality = False
			warning("skip centrality cut ({})".format(centrality))

		add_cut = True
		try:
			assert cut != "#"
		except AssertionError:
			warning("skip specific cut ({})".format(cut))
			add_cut = False

		if add_centrality is True:
			cut_update += " && {0}>{2} && {0}<{1}".format(
				self._centrality["branch"],
				self._centrality[centrality][0],
				self._centrality[centrality][1])
		if add_cut is True:
				cut_update += " && {0}".format(cut)
		return cut_update

	# ______________________________________
	def CreateBackgroundPDF(self, range):
		"""
		Configure and return the background PDF
		"""

		try:
			getattr(Models, self._fit_key['bkgr'])
		except AttributeError:
			error('''Cannot find {} in Ostap.FitModels
				for background function'''.format(self._fit_key['bkgr']))
			return None

		background = getattr(Models, self._fit_key['bkgr'])(
			'bkgr',
			mass=range)

		# Due to Ostap architectur, data members of PDF can't be set
		# after initiating the function. Therefor, one must find bellow
		# a mess to try to correctly create the background PDF object

		# ---- Configure Bkg_pdf ----
		if self._fit_key['bkgr'] == 'Bkg_pdf':

			# Default value
			param = {'power': 1}

			self.UpdateParameters(param)

			background = getattr(Models, self._fit_key['bkgr'])(
				'bkgr',
				mass=range,
				power=int(param['power']))
		else:
			warning(
				'{} has not default value setted, we encourage you to implement the code'
				.format(self._fit_key['bkgr']))

		return background

	# ______________________________________
	def CreateSignalPDF(self, range):
		"""
		Configure and return the signal PDF

		The method checks all the attributes from FitType
		string in the config file and set PDF object accordingly>
		See the code for available attributes to set
		"""

		# try to get the fit functions from Ostap
		try:
			getattr(Models, self._fit_key['signal'])
		except AttributeError:
			error('''Cannot find {} in Ostap.FitModels
				for signal function'''.format(self._fit_key['signal']))
			return None

		# Default PDF object
		sig = getattr(Models, self._fit_key['signal'])(
			'signal',
			mass=range,
			mean=self._mean_map[self._particle_name],
			sigma=self._width_map[self._particle_name])

		# Due to Ostap architectur, data members of PDF can't be set
		# after initiating the function. Therefor, one must find bellow
		# a mess to try to correctly create the background PDF object

		# ---- Configure CB2 ----
		if self._fit_key['signal'] == 'CB2_pdf':
			# Default value
			param = {
				'alL': ROOT.RooRealVar('aL', 'aL', 0.01, 0.5),
				'alR': ROOT.RooRealVar('aR', 'aR', 0.01, 0.5),
				'nL': ROOT.RooRealVar('nL', 'nL', 0.01, 0.5),
				'nR': ROOT.RooRealVar('nR', 'nR', 0.01, 0.5)}

			self.UpdateParameters(param)

			sig = getattr(Models, self._fit_key['signal'])(
				'signal',
				mass=range,
				mean=self._mean_map[self._particle_name],
				sigma=self._width_map[self._particle_name],
				alphaL=param['alL'],
				alphaR=param['alR'],
				nL=param['nL'],
				nR=param['nR'])

		# ---- Configure CrystalBall ----
		elif self._fit_key['signal'] == 'CrystalBall_pdf':
			# Default value
			param = {
				'alpha': ROOT.RooRealVar('alpha', 'alpha', 1.5, 2.5),
				'n': ROOT.RooRealVar('n', 'n', 0.5, 1.5)}

			self.UpdateParameters(param)

			sig = getattr(Models, self._fit_key['signal'])(
				'signal',
				mass=range,
				mean=self._mean_map[self._particle_name],
				sigma=self._width_map[self._particle_name],
				alpha=param['alpha'],
				n=param['n'])

		else:
			warning(
				'{} has not default value setted, we encourage you to implement the code'
				.format(self._fit_key['signal']))

		return sig

	# ______________________________________
	def DecodeFitType(self, fit_type):
		"""Decode the string containing all
			the information for the fit to be performed.

		The fit_type must be combination of key=value pairs separated by "|".
		Default keys are available in self._key_value

		Appart from the [signal] and [bkgr] keys, others have default values.
		If the key is different from standard key value it is assumed
		to be the value for a parameter of the fit function.

		Arguments:
			fit_type {str} -- example :
				particle=JPsi|leaf=jpsi_M|range=2;5|signal=CB2_pdf|bkgr=Bkg_pdf

		Returns:
			bool -- If the fit is correctly decoded
		"""

		# Always reset the data member at each fit_type
		self._fit_key["weight"] = 1

		if fit_type.count("signal") != 1 or fit_type.count("bkgr") != 1:
			error(
				"""Cannot decode type.
				Expecting 1 entries with 'signal' and 'bkgr, found {} and {}"""
				.format(
					fit_type.count("signal"),
					fit_type.count("bkgr")))
			return False

		# Check that keys appear only once in the string
		for x in self._fit_key.keys():
			try:
				assert fit_type.count(str(x + '=')) < 2
			except AssertionError:
				error(
					" Oups ! Multiple entries for {}, please fix it !"
					.format(x))
				return False

		# Fill self._fit_key and self._fit_attribute
		pairs = fit_type.split("|")
		for pair in pairs:
			key, value = self.GetKeyValue(pair, '=')

			try:
				assert key is not None or value is not None
			except AssertionError:
				error('Invalid key=value pair ' + pair)
			debug("key = %s, value = %s".format(key, value))

			self._fit_key[key] = value

		return True

	# ______________________________________
	def Fit(self, tuple, leaf, centrality, cut, fit_types, option):
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
			tuple {tuple}
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
		histos = self.GetHistos(tuple, leaf, centrality, cut)
		if histos is None:
			error("Cannot retrived histos for {}/{}/{}".format(leaf, centrality, cut))
			return None
		print(' --- histos retrived ...')
		debug("Fit: histos = {}".format(histos))

		# Construct our AnnaMuMuRestult for each histo or bins
		annaresults = [
			AnnaMuMuResult(self.GetBinType(), self.GetBinsAsString()[i])
			for i in range(0, len(histos))]

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
					.format(annaresult.GetName(), self.GetBinsAsString()[i], added_subresult))
			# Finally add result to spectra
			added_result += spectra.AdoptResult(annaresult, self.GetBinsAsString()[i])

		print(
			"number of results added for {} : {}"
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
			assert histo is not None
		except AssertionError:
			error("Cannot get histo")
			return None

		subresult_list = list()
		print(""" \n========= > Fit histo {} < ========= """.format(histo.GetName()))

		for i, fit_method in enumerate(fit_methods):
			# Get the fit configuration
			self.DecodeFitType(fit_method)

			# Redefine the fit range to the histo boundaries
			hmin = histo.GetXaxis().GetXmin()
			hmax = histo.GetXaxis().GetXmax()
			if 'range' in self._fit_key.keys():
				hmin = min(self._fit_key['range'])
				hmax = max(self._fit_key['range'])

			fit_range = ROOT.RooRealVar(
				histo.GetXaxis().GetName(),
				histo.GetXaxis().GetTitle(),
				hmin,
				hmax)

			# get PDF and create fit model
			signal = self.CreateSignalPDF(fit_range)
			if signal is None:
				continue
			background = self.CreateBackgroundPDF(fit_range)
			if background is None:
				continue

			# return None
			model = Models.Fit1D(signal=signal, background=background)

			data = ROOT.RooDataHist(
				histo.GetName(),
				histo.GetTitle(),
				ROOT.RooArgList(fit_range),
				histo)

			print(
				" \n------- > with {} + {} (weight = {} ) \n"
				.format(
					self._fit_key['signal'],
					self._fit_key['bkgr'],
					self._fit_key['weight']))

			result, frame = model.fitTo(
				data,
				silent=False,
				draw=True,
				refit=True,
				ncpu=8)
			debug("{}".format(result))

			# Create the AnnaMuMuResult
			sr_name = "{}_{}".format(fit_method, histo.GetName())
			sr = AnnaMuMuResult(name=sr_name, title=histo.GetTitle(), histo=histo)
			sr.weigth = self._fit_key['weight']
			sr.frame = frame
			for key in result.parameters().keys():
				sr.Set(key, result(key)[0].value(), result(key)[0].error())
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
				for j in range(1, len(self._binning[1][1:]))]
		else:
			return [
				[
					self._binning[i], self._binning[i + 1]
				] for i in range(1, len(self._binning[1:]))]

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
	def GetHistos(self, tuple, leaf, centrality, cut):
		"""Retrieve list of histograms

		All histograms are projected from the tuple
		according to each combination of centrality/cut/leaf/binning.

		Arguments:
			tuple {tuple} --
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
			assert tuple.GetLeaf(leaf) is not None
		except AssertionError:
			error("cannot find leaf {}".format(leaf))
			return None

		# This is just sweet :)
		histo_cuts = [
			self.ConfigureCuts(centrality, cut, bintype, bin_limits)
			for bin_limits in bin_all]
		debug("histo_cuts : {}".format(histo_cuts))

		for i, histo_cut in enumerate(histo_cuts):
			print(' --- Getting histo from leaf {} with cut {}'.format(leaf, histo_cut))
			histo = ROOT.TH1F(
				'histo', 'histo',
				100, tuple.GetMinimum(leaf) + 1, tuple.GetMaximum(leaf))
			tuple.Project('histo', leaf, histo_cut)
			# command = '{}>>histo'.format(leaf)
			# tuple.Draw(command, histo_cut, "goff")

			# try:
			# 	assert ROOT.gDirectory.Get("histo") is not None
			# except AssertionError:
			# 	error("cannot get histo from leaf {} ... continue".format(leaf))
			# 	continue

			try:
				assert histo.GetEntries() > 0
			except AssertionError:
				error("could not get histo with cut {}".format(histo_cut))
				continue
			histo_list.append(histo)
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
	def SetAdditionalAttributeToModel(self, model):
		"""Run over self._fit_key and try to configure
		fit model if possible

		Arguments:
			model {Ostap.FitModels} --
		"""

		# Check if attribute belong to the model itself and set it if true
		for i, attribute in enumerate(self._fit_key.keys()):
			if attribute in ['signal', 'bkgr', 'weight']:
				continue
			try:
				getattr(model, attribute)
			except AttributeError:
				debug(
					'''No {} in the background part of the model'''
					.format(attribute))
				continue
			info(
				'Set attribute {} = {} to model'
				.format(attribute, self._fit_key[attribute]))

			# Set attribute according to if it is a range or not
			if ';' in self._fit_key[attribute]:
				varmin = float(min(self._fit_key[attribute].split(';')))
				varmax = float(max(self._fit_key[attribute].split(';')))
				var = ROOT.RooRealVar(
					self._particle_name + '_' + attribute,
					self._particle_name + '_' + attribute,
					varmin,
					varmax)
				setattr(model, attribute, var)
			else:
				setattr(model, attribute, self._fit_key[attribute])

	# ______________________________________
	def UpdateParameters(self, param):
		"""
		Change the parameters value of the fit
		if there are entries related to sig PDF in the fit keys
		"""

		for i, attribute in enumerate(self._fit_key.keys()):
			if attribute in param.keys():
				# Set attribute according to if it is a range or not
				if ';' in self._fit_key[attribute]:
					varmin = float(min(self._fit_key[attribute].split(';')))
					varmax = float(max(self._fit_key[attribute].split(';')))
					var = ROOT.RooRealVar(
						attribute,
						attribute,
						varmin,
						varmax)
					param[attribute] = var
				else:
					param[attribute] = float(self._fit_key[attribute])

				info(
					'Change default value of {} (= {}) for signal PDF'
					.format(attribute, self._fit_key[attribute]))


# =============================================================================
# The END
# =============================================================================
