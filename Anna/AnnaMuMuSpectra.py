# =============================================================================
#  @class AnnaMuMuFacade
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30

from logging import debug, error, warning
from .AnnaMuMuConfig import SetCanvasStyle
import ROOT
import math


class AnnaMuMuSpectra():
	"""Container for AnnaMuMuResult

	AnnaMuMuResults are stored according to a specific binning into a TObjArray.

	Extends:
		TNamed
	"""

	# ______________________________________
	def __init__(self, name, title):
		""" cstr """

		self.name = name
		self.title = title
		self.results = dict()  	# where are stored the AnnaMuMuResults

	# ______________________________________
	def AdoptResult(self, result, bin):
		""" adopt (i.e. we are becoming the owner) a result for a given bin"""

		if result is None:
			error("Cannot adopt a null result list")
			return 0

		debug("result : {}".format(result))
		sizeBeforeAdd = len(self.results)
		self.results[str(bin)] = result  # Add the result for a given bin type
		sizeAfterAdd = len(self.results)

		if sizeBeforeAdd >= sizeAfterAdd:
			error("Error adopting result {} to spectra {}".format(
				result.GetName(),
				self.GetName()))
			return 0

		else:
			print(" --- result {} (bin {}) adopted !".format(result.GetName(), str(bin)))
			return 1

	# ______________________________________
	def DrawResults(self, particle_name, subresults):
		"""Draw the results on a TCanvas

		Arguments:
			particle_name {str} -- the result itself
			subresults {list} -- specific list of subresults
		"""

		frame_list = list()
		quantity = list()

		for bin in self.results.keys():
			result = self.results[bin]
			if result is None:
				warning(
					'Cannot find result for bin {}, continue ...'
					.format(bin))
				continue

			# loop over subresults
			for srname in result.subresults:
				subresult = result.subresults[srname]
				if subresults is not None and subresult.name not in subresults:
					continue

				if subresult.frame is not None:
					frame_list.append(subresult.frame)
				else:
					warning(
						'Cannot find frame in subresult {}'
						.format(subresult.name))
					continue

				quantity.append(
					[
						'S',
						subresult.GetValue('S'),
						subresult.GetErrorStat('S')
					]) if subresult.HasValue('S') > 0 \
					else quantity.append(['S', 0., 0.])

				quantity.append(
					[
						'mean_signal',
						subresult.GetValue('mean_signal'),
						subresult.GetErrorStat('mean_signal')
					]) if subresult.HasValue('mean_signal') > 0 \
					else quantity.append(['mean_signal', 0., 0.])

				quantity.append(
					[
						particle_name + "_sigma",
						subresult.GetValue(particle_name + "_sigma"),
						subresult.GetErrorStat(particle_name + "_sigma")
					]) if subresult.HasValue(particle_name + "_sigma" > 0)\
					else quantity.append([particle_name + "_sigma", 0., 0.])

		if len(frame_list) == 0:
			error('Cannot retrived any frame')
			return

		# Configure canvas
		nx, ny = 1, 1
		nofResult = len(frame_list)
		if nofResult == 2:
			nx = 2
			ny = 0

		elif nofResult > 2:
			ny = int(round((math.sqrt(nofResult)), 1))
			nx = int(round(((nofResult / ny) + 0.6), 1))

		c = ROOT.TCanvas()
		ROOT.SetOwnership(c, False)
		SetCanvasStyle(c)
		c.Divide(nx, ny, 0, 0)
		c.SetTitle("{}".format(self.name))
		c.DrawClone()

		for i, frame in enumerate(frame_list):
			c.cd(i + 1)
			frame.Draw('same')

			# --- Config. first legend pad ---
			leg = ROOT.TLegend(0.5209804, 0.2662884, 0.7326179, 0.7057458)
			leg.SetTextSize(0.05)
			leg.SetBorderSize(0)

			for q in quantity:
				leg.AddEntry(
					ROOT.TObject(),
					'{} : {} +- {}'.format(q[0], q[1], q[2]))
			leg.Draw("same")

	# ______________________________________
	def GetBins(self):
		return self.results.keys()

	# ______________________________________
	def GetResults(self):
		return self.results

	# ______________________________________
	def GetResultsForBin(self, bin):
		return self.results[bin]

	# ______________________________________
	def GetName(self):
		return self.name

	# ______________________________________
	def GetTitle(self):
		return self.title

# =============================================================================
# The END
# =============================================================================
