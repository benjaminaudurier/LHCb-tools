# =============================================================================
#  @class AnnaMuMuResult
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 

from ROOT import TNamed
import math
from enum import Enum
from logging import debug


# ______________________________________
class MergingMethod(Enum):
	kMean = 0,
	kSum = 1


# ______________________________________
class Index(Enum):
	kValue = 0,
	kStat = 1,
	kSys = 2


# ______________________________________
class AnnaMuMuResult(TNamed):
	"""Store results for the Anna framework
	
	Base class to hold a set of results of the same quantity,
	computed using various methods, each with their errors.
	A AnnaMuMuResult can hold other AnnaMuMuResult, refered as
	subresults later.
	
	Extends:
		TNamed
	"""

	# ______________________________________
	def __init__(self, name, title, histo=None):
		"""cstr
				
		Arguments:
			name {str{}} -- 
			title {str{}} -- 
		
		Keyword Arguments:
			histo {TH1} -- (default: {None})
		"""

		# General for all AnnaMuMuResult
		TNamed.__init__(self, name, title)
		self._subresults = None  # dict()
		self._subresults_to_be_incuded = None  # list()
		
		# How to merge quantity for subresults 
		self._mergingMethod = MergingMethod  
		self._resultMergingMethod = self._mergingMethod.kMean
		
		# Will be define only if self is a sub-result
		self._binning = None
		self._histo = histo
		self._index = Index
		self._map = None
		self._weigth = 1.

	# ______________________________________
	def AdoptSubResult(self, result_list):
		"""Adopt all results in the result list
				
		Arguments:
			result_list {list()} -- Must contains AnnaMuMuResults
		
		Returns:
			int -- number of subresults stored
		"""

		if self._subresults is None:
			self._subresults = dict()

		subresultsBeforeAdd = len(self._subresults)
		for r in result_list:
			self._subresults[r.GetName()] = r
			self.SubResultsToBeIncluded().append(r.GetName())
		subresultsAfterAdd = len(self._subresults)

		if subresultsBeforeAdd < subresultsAfterAdd: 
			return subresultsAfterAdd - subresultsBeforeAdd
		else: 
			return 0

	# ______________________________________
	def DeleteEntry(self, entry):
		"""Delete entry in self._subresults_to_be_incuded
				
		Arguments:
			entry {str{}} --
		"""

		while True:
			try:
				self._subresults_to_be_incuded.remove(entry)
			except ValueError:
				return

	# ______________________________________
	def ErrorAB(a, aerr, b, berr):
		"""
		Compute square root of the quadratic sum
		"""
		e = 0.0

		if math.fabs(a) > 1E-12:
			e += aerr * aerr / (a * a)

		if math.fabs(a) > 1E-12:
			e += (berr * berr) / (b * b)

		return math.sqrt(e)

	# ______________________________________
	def Exclude(self, sub_result_list):
		""" Exclude some subresult names from the list of subresult
		to be used when computing the mean of a value 
				
		Arguments:
			sub_result_list {list()} -- 
		"""

		slist = sub_result_list

		to_be_excluded = self.GetSubResultNameList()

		if slist == "*":
			self.Exclude(to_be_excluded)
			return
		
		if self.self._subresult is not None:
			a = slist.split(",")

			for s in a:
				self.DeleteEntry(a)
	
	# ______________________________________
	def GetErrorStat(self, name, subresult_name):
		"""Get the stat. error of a value (either directly 
		or by computing the mean of the subresults).

		Default method is mean, but it can be changed with a different settings
		of self._resultMergingMethod
				
		Arguments:
			name {str{}} -- Name of the variable
			subresult_name {str{}} -- subresult name
		
		Returns:
			number -- None in case of error
		"""

		# If we specify a subresults
		if len(subresult_name) > 0:

			if not self._subresult:

				print("No subresult from which \
						I could get the {} one...".format(subresult_name))
				return None

			sub = self._subresult[subresult_name]
			if not sub:
				print("No subresult from which \
						I could get the {} one...".format(subresult_name))
				return None

			return sub.GetErrorStat(name)

		# self._map existes only for AnnaMuMuResults w/o subresults
		if self._map is not None:
			error_stat = self._map[name][self._index.kStat]
			return error_stat

		# Mean method (by default)
		if self._resultMergingMethod == self._mergingMethod.kMean:

			n, werr, sumw = 0, 0., 0.

			for r in self._subresults:
				if self.IsIncluded(r.GetName()) is True and r.HasValue(name):

					"""
					The stat. error is just a weighted mean of all the stat. error.
					"""

					# Check fit status
					fitStatus = r.HasValue("FitResult") \
						if r.GetValue("FitResult") is not None else 0
					covStatus = r.HasValue("CovMatrixStatus") \
						if r.GetValue("CovMatrixStatus") is not None else 3
					chi2 = r.HasValue("FitChi2PerNDF") \
						if r.GetValue("FitChi2PerNDF") is not None else 1

					# Select only Fit that converge
					if (fitStatus != 0 and fitStatus != 4000) or chi2 > 2.5:
						debug("Fit {} excluded (FitResult = {} | Cov. Mat. = {})\n".format(
							r.GetName(), fitStatus, covStatus)
						)
						continue
					
					# weight and error
					w, err = r.Weight(), r.GetErrorStat(name)
					debug(" --- Weight for subResults {} = {} \n".format(r.GetName(), w))
					debug(" --- FitStatus for subresult : {}".format(r.GetValue("FitStatus")))
					# If the error is not correct we skip the subresult
					if err < 0:
						debug(" --- subResults {} has a negative error stat \n".format(
							r.GetName(), err)
						)
						
					# stat and sum of weight
					werr += w * err
					sumw += w
					n += 1
			
			# Case something went wrong
			try:
				assert n > 1
			except AssertionError:
				return None
			# case we have one single results
			if n == 1:
				for r in self._subresults:
					if self.IsIncluded(r.GetName()) is True and r.HasValue(name):
						return r.GetErrorStat(name)			

			return werr / sumw

		else:
			n, sm, sme2 = 0, 0., 0.
			for r in self._subresults:
				if self.IsIncluded(r.GetName()) is True and r.HasValue(name):			  
					err = r.GetErrorStat(name) / r.GetValue(name)
					
					sme2 += err * err
					sm += r.GetValue(name)
					++n
			if n > 0:
				return sm * math.sqrt(sme2)
			else:
				return None

	# ______________________________________
	def GetRMS(self, name, subresult_name):
		"""Compute the rms of the subresults.
		
		Arguments:
			name {str{}} -- Name of the variable
			subresult_name {str{}} -- subresults
		
		Returns:
			number -- 0 in case of problem
		"""

		# If we specify a subresults
		if len(subresult_name) > 0:

			if not self._subresult:

				print("No subresult from which \
						I could get the {} one...".format(subresult_name))
				return 0

			sub = self._subresult[subresult_name]
			if not sub:
				print("No subresult from which \
						I could get the {} one...".format(subresult_name))
				return 0

			return sub.GetRMS(name)

		# self._map existes only for AnnaMuMuResults w/o subresults
		if self._map is not None:
			error_sys = self._map[name][self._index.kSys]
			return error_sys if error_sys is not None else 0.0

		v1, v2, sm = 0., 0., 0.
		n = 0
		xmean = self.GetValue(name)

		for r in self._subresults:
			if self.IsIncluded(r.GetName()) is True and r.HasValue(name):

				"""
				The weight for each subresult is the same (=1.), since the data sample 
				is always the same and just the fit function changes among subresults.
				We can also use 1./err/err/wstat  where wstat = 1. / val as stat. 
				wstat was not there before and
				was introduced to remove the dependence 
				of the error with the Nof extracted Jpsi 
				(valid only for counts results with different data samples 
				and not for <pt>...)
				"""

				# Check fit status
				fitStatus = r.HasValue("FitResult") \
					if r.GetValue("FitResult") is not None else 0
				covStatus = r.HasValue("CovMatrixStatus") \
					if r.GetValue("CovMatrixStatus") is not None else 3
				chi2 = r.HasValue("FitChi2PerNDF") \
					if r.GetValue("FitChi2PerNDF") is not None else 1

				# Select only Fit that converge
				if (fitStatus != 0 and fitStatus != 4000) or chi2 > 2.5:
					debug("Fit {} excluded (FitResult = {} | Cov. Mat. = {})\n".format(
						r.GetName(),
						fitStatus,
						covStatus)
					)
					continue

				wi = r.Weight()
				v1 += wi
				v2 += wi * wi
				diff = r.GetValue(name) - xmean
				sm += wi * diff * diff
				n += 1
		
		# Case something went wrong
		try:
			assert n > 1
		except AssertionError:
			return 0.0
		# case we have one single results
		if n == 1:
			for r in self._subresults:
				if self.IsIncluded(r.GetName()) is True and r.HasValue(name):
					return r.GetRMS(name)			

		unbiased = math.sqrt((v1 / (v1 * v1 - v2)) * sm)
		biased = math.sqrt(sm / v1)
		debug(
			" ----> v1 {} v1*v1 {} v2 {} -> biased {} unbiased {} (ratio {}) \n".format(
				v1,
				v1 * v1,
				v2,
				biased,
				unbiased,
				unbiased / biased
			)
		)

		return unbiased

	# ______________________________________
	def GetSubResultNameList(self):
		"""Get a comma separated list of our subresult aliases
		"""
		subresult_name_list = ''

		for result in self._subresults:
			if len(subresult_name_list) > 0: 
				subresult_name_list += ","

			subresult_name_list += result.GetName()
		
		return subresult_name_list

	# ______________________________________
	def GetValue(self, name, subresult_name):
		"""Get a value (either directly or by computing the mean of the subresults).
				
		Default method is mean, but it can be changed with a different settings
		of self._resultMergingMethod
				
		Arguments:
			name {str{}} -- Name of the variable
			subresult_name {str{}} -- subresult name
		
		Returns:
			number -- None in case of error
		"""

		# If we specify a subresults
		if len(subresult_name) > 0:

			if not self._subresult:
				print("No subresult from which \
						I could get the {} one...".format(subresult_name))
				return None

			sub = self._subresult[subresult_name]

			if not sub:
				print("No subresult from which \
						I could get the {} one...".format(subresult_name))
				return None

			return sub.GetValue(name)

		# self._map existes only for AnnaMuMuResults w/o subresults
		if self._map is not None:
			value = self._map[name][self._index.kValue]
			return value

		# Mean method (by default)
		if self._resultMergingMethod == self._mergingMethod.kMean:

			mean, sm = 0, 0., 0.

			for r in self._subresults:
				if self.IsIncluded(r.GetName()) is True and r.HasValue(name):

					""" 
					The weight for each subresult is the same (=1.), since the data sample 
					is always the same and just the fit function changes among subresults.
					We can also weight subresults with :
						e = r.GetErrorStat(name)/math.sqrt(r.GetValue(name))

					The math.sqrt(r>GetValue(name)) was not there before and was introduced 
					to remove the dependence of the error with the number of particule 
					extracted (valid only for counts results with different data samples 
					and not for <pt>...)
					"""

					# Check fit status
					fitStatus = r.HasValue("FitResult") \
						if r.GetValue("FitResult") > 0 else 0
					covStatus = r.HasValue("CovMatrixStatus") \
						if r.GetValue("CovMatrixStatus") > 0 else 3
					chi2 = r.HasValue("FitChi2PerNDF") \
						if r.GetValue("FitChi2PerNDF") > 0 else 1

					# Select only Fit that converge
					if (fitStatus != 0 and fitStatus != 4000) or chi2 > 2.5:
						debug("Fit {} excluded (FitResult = {} | Cov. Mat. = {})\n".format(
							r.GetName(), fitStatus, covStatus)
						)
						continue
					
					# weight and error
					w = r.Weight()
					debug(" --- Weight for subResults {} = {} \n".format(r.GetName(), w))
					# If the error is not correct we skip the subresult
					if r.GetErrorStat(name) < 0.0 or r.GetValue("FitStatus") != 0:
						continue
					mean += w * r.GetValue(name)
					sm += w
								
			# Case something went wrong
			try:
				assert sm != 0.
			except AssertionError:
				return None

			return mean / sm

		else:
			sm = 0.
			for r in self._subresults:
				if self.IsIncluded(r.GetName()) is True and r.HasValue(name):			  
					sm += r.GetValue(name)
			
			# Case something went wrong
			try:
				assert sm != 0.
			except AssertionError:
				return None

			return sm

	# ______________________________________
	def HasValue(self, name, subresult_name):
		"""
			Whether this result (or subresult if subresult_name is provided) 
			has a property named "name"
			When having subresults, return the number of subresults that have this value
		"""
		if len(subresult_name) > 0:
			if self._subresults is None:
				print("Error : No subresults from which \
				I could get the {} one...".format(subresult_name))
				return False
		
		try:
			sub = self._subresults[subresult_name]
		except KeyError:
			print("Error : Could not get subresult named " + subresult_name)
			return False

		return sub.HasValue(name)

		# No _subresults if results contains subresults
		if self._subresults is not None:
			try:
				self._subresults[subresult_name]
			except KeyError:
				print(
					"Error : Could not get subresult named " 
					+ subresult_name 
					+ " from map"
				)
				return False
			return True

		n = 0
		for r in self._subresults:			 
			if r.HasValue(name) is True: 
				n += 1

		return n

	# ______________________________________
	def Include(self, sub_result_list):
		"""
		(re)include some subresult names
		"""
		if len(sub_result_list) == 0:
			self.Exclude("*")
			return

		if sub_result_list == '*':
			sub_result_list = self.GetSubResultNameList()

		a = sub_result_list.split(',')
		for s in a:
			if self._subresults_to_be_incuded is None:
				self._subresults_to_be_incuded = list()

			if self.IsIncluded(s) is False:
				self._subresults_to_be_incuded.append(s)

	# ______________________________________
	def IsIncluded(self, alias):
		""" 
		whether that subresult alias should be included when computing means, etc...
		"""

		if self._subresults_to_be_incuded is None: 
			return True
		
		try:
			assert self._subresults_to_be_incuded.count(alias) == 1
		except AssertionError:
			return False
		
		return True

	# ______________________________________
	def Print(self, opt):
		"""
		printout
		"""	
		option = opt
		for x in range(0, 9): 
			option = option.replace(str(x), '')
		poption = option
		poption.replace("ALL", '')
		poption.replace("FULL", '')

		print(poption + " ")

		print("{} {} {}".format(
			self.GetName(),
			self.GetTitle(),
			" WEIGHT {}".format(self._weigth)) if self._weigth > 0.0 else "" 
		)

		if self._subresults is not None and len(self._subresults) > 1:
			print(" (" + len(self._subresults) + " subresults)")

		print("")

		nsub = len(self._subresults) if self._subresults is not None else 0
		if self._map is not None:
			for key in self._map.keys():
				if nsub == 0 or nsub == self.HasValue(key):
					self.PrintValue(
						key,
						poption,
						self.GetValue(key),
						self.GetErrorStat(key),
						self.GetRMS
					) 

		if self._subresults is not None and \
			(option.count('ALL') > 1 or option.count('FULL') > 1):
			
			print(poption + '\t===== sub results ===== ')
			option += "\t\t"

			for r in self._subresults:
				if self.IsIncluded(r.GetName()) is False:
					print(" [EXCLUDED]")
				r.Print(option)

	# ______________________________________
	def PrintValue(self, key, opt, value, errorStat, rms):
		""" 
		print one value and its associated error
		"""

		if key.count('AccEff') > 1:
			print(opt + "\t\t%20s %9.2f +- %5.2f %% (%5.2f %%)".format(
				key,
				value * 100,
				errorStat * 100,
				errorStat * 100.0 / value if value != 0.0 else 0.0)
			)

			if rms is not None:
				print(" RMS %9.2f (%5.2f %%)".format(rms, 100.0 * rms / value))
			print("")

		elif key.count('Sigma') > 1 or key.count('Mean') > 1:
			print(opt + "\t\t%20s %9.2f +- %5.2f (%5.2f %%) MeV/c^2".format(
				key,
				value * 1E3,
				1E3 * errorStat,
				errorStat * 100.0 / value if value != 0.0 else 0.0)
			)

			if rms is not None:
				print(" RMS %9.2f (%5.2f %%)".format(rms, 100.0 * rms / value))
			print("")

		elif key.count('Nof') > 1:
			print(opt + "\t\t%20s %9.3f +- %5.3f (%5.3f %%) MeV/c^2".format(
				key,
				value * 1E3,
				1E3 * errorStat,
				errorStat * 100.0 / value if value != 0.0 else 0.0)
			)

			if rms is not None:
				print(" RMS %9.2f (%5.2f %%)".format(rms, 100.0 * rms / value))
			print("")

		elif value > 1E-3 and value < 1E3:
			if errorStat > 0.0:
				print(opt + "\t\t%20s %9.3f +- %5.3f (%5.3f %%) MeV/c^2".format(
					key,
					value * 1E3,
					1E3 * errorStat,
					errorStat * 100.0 / value if value != 0.0 else 0.0)
				)

				if rms is not None:
					print(" RMS %9.2f (%5.2f %%)".format(rms, 100.0 * rms / value))

			else:
				print(opt + "\t\t%20s %9.3f".format(key, value))
			print("")

		else:
			if errorStat > 0.0:
				print(opt + "\t\t%20s %9.2e +- %5.2e (%5.2f %%) MeV/c^2".format(
					key,
					value * 1E3,
					1E3 * errorStat,
					errorStat * 100.0 / value if value != 0.0 else 0.0)
				)

				if rms is not None:
					print(" RMS %9.2e (%5.2f %%)".format(rms, 100.0 * rms / value))

			else:
				print(opt + "\t\t%20s %9.2e".format(key, value))
			print("")

	# ______________________________________
	def Scale(self, w):
		"""
		scale all our internal values by w
		"""
		for key in self._map.keys():
			value = self.GetValue(key)
			error = self.GetErrorStat(key)
			rms = self.GetRMS(key)

			self.Set(key, value * w, error * w, rms * w)

	# ______________________________________
	def Set(self, name, value, errorStat, rms):
		""" 
		Set a (value,error) pair with a given name
		"""
		if self._map is None: 
			self._map = dict()
		try:
			p = self._map[name]
		except NameError:
			p = [value, errorStat, rms]
			self._map[name] = p

		p[self._index.kValue] = value
		p[self._index.kErrorStat] = errorStat
		p[self._index.kRMS] = rms

	# ______________________________________
	def SubResult(self, subresult_name):
		"""
		get a given subresult
		"""
		if self._subresults is None: 
			return None
		
		for r in self._subresults:
			if r.GetName() == subresult_name: 
				return r

		return None

	# ______________________________________
	def SubResultsToBeIncluded(self):
		if self._subresults_to_be_incuded is None:
			self._subresults_to_be_incuded = list()
		return self._subresults_to_be_incuded

# =============================================================================
# The END 
# =============================================================================	 