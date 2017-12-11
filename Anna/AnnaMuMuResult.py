# =============================================================================
#  @class AnnaMuMuResult
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30 

from ROOT import TObject, TObjArray, TList, TObjString, TMath
import math
from enum import Enum
import logging.debug as debug

class AnnaMuMuResult(TObject):
	"""[summary]
	
	[description]
	
	Extends:
		TObject
	"""

	# ______________________________________
	def __init__(self, name, title):
		self._name = name
		self._title = title
		self._subresults = None  # dict()
		self._subresults_to_be_incuded = None  # dict()
		self._map = None
		self._index = Enum('kValue', 'kStat', 'kSys')
		self._mergingMethod = Enum('kMean', 'kSum')
		self._resultMergingMethod = self._mergingMethod('kMean')

	# ______________________________________
	def AdoptSubResult(self, r):
		# ==== TObjArray version 
		# if self._subresults is None:
		# 	self._subresults = TObjArray()
		# 	self._subresults.SetOwner(True)

		# subresultsBeforeAdd = self._subresults.GetEntriesFast()
		# self._subresults.Add(r)
		# subresultsAfterAdd = self._subresults.GetEntriesFast()

		# self.SubResultsToBeIncluded().Add(TObjString(r.Alias()))

		# ==== Version with dict =====
		if self._subresults is None:
			self._subresults = dict()

		subresultsBeforeAdd = len(self._subresults)
		self._subresults[r.GetName()] = r
		subresultsAfterAdd = len(self._subresults)

		self.SubResultsToBeIncluded()[r.GetName()]

		if subresultsBeforeAdd < subresultsAfterAdd: 
			return True
		else: 
			return False

	# ______________________________________
	def DeleteEntry(self, entry):

		while True:
			try:
				self._subresults_to_be_incuded.remove(entry)
			except ValueError:
				return

	# ______________________________________
	def ErrorAB(a, aerr, b, berr):

		e = 0.0

		if math.fabs(a) > 1E-12:
			e += aerr * aerr / (a * a)

		if math.fabs(a) > 1E-12:
			e += (berr * berr) / (b * b)

		return math.sqrt(e)

	# ______________________________________
	def Exclude(self, subResultList):
		""" 
			exclude some subresult names from the list of subresult
			to be used when computing the mean 
		"""

		slist = subResultList

		to_be_excluded = self.GetSubResultNameList()

		if slist == "*":
			self.Exclude(to_be_excluded)
			return
		
		if self.self._subresult is not None:
			a = slist.split(",")

			for s in a:
				self.DeleteEntry(a)
	
	# ______________________________________
	def GetErrorStat(self, name, subResultName):

		"""    
		compute the mean error value from all subresults that are included
		return imaginary if any problem
		
		"""

		# If we specify a subresults
		if len(subResultName) > 0:

			if not self._subresult:

				print "No subresult from which \
						I could get the {} one...".format(subResultName)
				return 1j

			sub = self._subresult[subResultName]
			if not sub:
				print "No subresult from which \
						I could get the {} one...".format(subResultName)
				return 1j

			return sub.GetErrorStat(name)

		# self._map existes only for AnnaMuMuResults w/o subresults
		if self._map is not None:
			error_stat = self._map(self._index('kStat'))
			return error_stat

		# Mean method (by default)
		if self._resultMergingMethod == self._mergingMethod('kMean'):

			n, werr, sumw = 0, 0., 0.

			for r in self._subresults:
				if self.IsIncluded(r.GetName()) is True and r.HasValue(name):

					"""
					The stat. error is just a weighted mean of all the stat. error.
					"""

					# Check fit status
					fitStatus = r.HasValue("FitResult") if r.GetValue("FitResult") else 0
					covStatus = r.HasValue("CovMatrixStatus") if r.GetValue("CovMatrixStatus") else 3
					chi2 = r.HasValue("FitChi2PerNDF") if r.GetValue("FitChi2PerNDF") else 1

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
				return 1j
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
				return 1j

	# ______________________________________
	def GetRMS(self, name, subResultName):

		"""
			compute the rms of the subresults
			returns zero if no subresults
		"""

		# If we specify a subresults
		if len(subResultName) > 0:

			if not self._subresult:

				print "No subresult from which \
						I could get the {} one...".format(subResultName)
				return 0

			sub = self._subresult[subResultName]
			if not sub:
				print "No subresult from which \
						I could get the {} one...".format(subResultName)
				return 0

			return sub.GetRMS(name)

		# self._map existes only for AnnaMuMuResults w/o subresults
		if self._map is not None:
			error_sys = self._map(self._index('kSys'))
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
				fitStatus = r.HasValue("FitResult") if r.GetValue("FitResult") else 0
				covStatus = r.HasValue("CovMatrixStatus") if r.GetValue("CovMatrixStatus") else 3
				chi2 = r.HasValue("FitChi2PerNDF") if r.GetValue("FitChi2PerNDF") else 1

				# Select only Fit that converge
				if (fitStatus != 0 and fitStatus != 4000) or chi2 > 2.5:
					debug("Fit {} excluded (FitResult = {} | Cov. Mat. = {})\n".format(
						r.GetName(), fitStatus, covStatus)
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

		debug(" ----> v1 {} v1*v1 {} v2 {} -> biased {} unbiased {} (ratio {}) \n".format(
			v1,
			v1 * v1,
			v2,
			biased,
			unbiased,
			unbiased / biased)
		)

		return unbiased

	# ______________________________________
	def GetSubResultNameList(self):
		"""
			get a comma separated list of our subresult aliases
		"""
		subresult_name_list = ''

		for result in self._subresults:
			if len(subresult_name_list) > 0: 
				subresult_name_list += ","

			subresult_name_list += result.GetName()
		
		return subresult_name_list

	# ______________________________________
	def GetValue(self, name, subResultName):

		"""    
		get a value (either directly or by computing the mean of the subresults)
		return imaginary if any problem
		"""

		# If we specify a subresults
		if len(subResultName) > 0:

			if not self._subresult:
				print "No subresult from which \
						I could get the {} one...".format(subResultName)
				return 1j

			sub = self._subresult[subResultName]

			if not sub:
				print "No subresult from which \
						I could get the {} one...".format(subResultName)
				return 1j

			return sub.GetValue(name)

		# self._map existes only for AnnaMuMuResults w/o subresults
		if self._map is not None:
			value = self._map(self._index('kValue'))
			return value

		# Mean method (by default)
		if self._resultMergingMethod == self._mergingMethod('kMean'):

			mean, sm = 0, 0., 0.

			for r in self._subresults:
				if self.IsIncluded(r.GetName()) is True and r.HasValue(name):

					""" 
					The weight for each subresult is the same (=1.), since the data sample 
					is always the same and just the fit function changes among subresults.
					We can also weight subresults with :
						e = r.GetErrorStat(name)/math.sqrt(r.GetValue(name))

					The math.sqrt(r>GetValue(name)) was not there before and was introduced 
					to remove the dependence of the error with the Number of particule extracted 
					(valid only for counts results with different data samples and not for <pt>...)
					"""

					# Check fi status
					fitStatus = r.HasValue("FitResult") if r.GetValue("FitResult") else 0
					covStatus = r.HasValue("CovMatrixStatus") if r.GetValue("CovMatrixStatus") else 3
					chi2 = r.HasValue("FitChi2PerNDF") if r.GetValue("FitChi2PerNDF") else 1

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
				return 1j

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
				return 1j

			return sm

	# ______________________________________
	def IsIncluded(self, alias):
		""" 
		whether that subresult alias should be included when computing means, etc...
		"""

		if self._subresults_to_be_incuded is not None: 
			return True

		try:
			self._subresults_to_be_incuded[alias]
		except KeyError:
			return False
		
		return True

	# ______________________________________
	def SubResultsToBeIncluded(self):
		if self._subresults_to_be_incuded is None:
			self._subresults_to_be_incuded = dict()
		return self._subresults_to_be_incuded

