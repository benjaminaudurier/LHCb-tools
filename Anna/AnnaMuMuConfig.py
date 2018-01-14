# =============================================================================
## @class AnnaMuMuConfig
#  helper class to store steering options for other Anna classes
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30
from logging import debug, warning
import ROOT

class AnnaMuMuConfig:
	"""Helper class to store steering options for other Anna classes

	This class reads an extern text file and store info in a dictionnary.
	Each line of the config file should be written as <key> : <value>
	"""

	# ______________________________________
	def __init__(self):
		""" cstr """
		self._map = dict()
		self._key = (
			"Centrality",
			"CutCombination",
			"FitType",
			"MotherLeaf",
			"MuplusLeaf",
			"MuminusLeaf",
			"ResultFilePath")

	# ______________________________________
	def ReadFromFile(self, configfile=""):
		"""Read the configuration file and set tuples with correct entries.

		All lines in the file should be written as <key> : <value>>
		example:
			#Centrality: ALL
			MotherLeaf: JPSI_M
			#CutCombination: 2.5<JPSI_Y&&JPSI_Y<4

		Automatically skip empty line and line starting with '#'

		Keyword Arguments:
			configfile {str} -- file name (default: {""})

		Returns:
			bool -- weither or not the function succeeded
		"""

		with open(configfile, "r") as file:
			lines = file.readlines()

			for key_name in self._key:
				entries = []

				# Find and store all the entries for a given key
				for line in lines:
					debug("Reads line {}".format(line))
					if line == '' or line.startswith('#') is True:
						continue
					key, value = self.DecodeLine(line)
					if key == key_name:
						entries.append(value)

				# Add to map
				if len(entries) > 0:
					self._map[key_name] = entries
				else:
					warning("No entries for key {}, set default".format(key_name))
					self._map[key_name] = self.GetDefaultEntry(key_name)

			return True

	# ______________________________________
	def GetCentrality(self):
		return self._map["Centrality"]

	# ______________________________________
	def GetCutCombination(self):
		return self._map["CutCombination"]

	# ______________________________________
	def GetFitType(self):
		return self._map["FitType"]

	# ______________________________________
	def GetMotherLeaf(self):
		return self._map["MotherLeaf"]

	# ______________________________________
	def GetMuonPlusLeaf(self):
		return self._map["MuplusLeaf"]

	# ______________________________________
	def GetMuonMinusLeaf(self):
		return self._map["MuminusLeaf"]

	# ______________________________________
	def GetResultFilePath(self):
		return self._map["ResultFilePath"]

	# ______________________________________
	def GetDefaultEntry(self, key_name):
		return "#"

	# ______________________________________
	def PrintKey(self):
		print(self._key)

	# ______________________________________
	def PrintMap(self):
		print(self._map)

	# ______________________________________
	def DecodeLine(self, line=""):
		"""Decode a line

		Inner functions to get key : value pair from
		configuration file

		Keyword Arguments:
			line {str} -- the line to read (default: {""})

		Returns:
			{str}, {str} -- key, value
		"""
		split_line = line.replace(" ", "")
		split_line = split_line.strip()
		split_line = split_line.split(":")

		# check the len
		try:
			assert len(split_line) == 2
		except AssertionError:
			print("Format of {} in config file is not correct, should be \"key:values \"".format(line))
			return "", ""

		debug("key: {} / value: {}".format(split_line[0], split_line[1]))

		return split_line[0], split_line[1]

# ______________________________________
def SetCanvasStyle(canvas):
	"""
	Default configuration for TCanvas
	"""
	ROOT.gStyle.SetOptStat(0)
	ROOT.gStyle.SetOptTitle(0)

	font = 42

	ROOT.gROOT.SetStyle("Plain")
	ROOT.gStyle.SetFrameBorderMode(0)
	ROOT.gStyle.SetFrameFillColor(0)
	ROOT.gStyle.SetCanvasBorderMode(0)
	ROOT.gStyle.SetPadBorderMode(0)
	ROOT.gStyle.SetPadColor(10)
	ROOT.gStyle.SetCanvasColor(10)
	ROOT.gStyle.SetTitleFillColor(10)
	ROOT.gStyle.SetTitleBorderSize(1)
	ROOT.gStyle.SetStatColor(10)
	ROOT.gStyle.SetStatBorderSize(1)
	ROOT.gStyle.SetLegendBorderSize(1)
	ROOT.gStyle.SetDrawBorder(0)
	ROOT.gStyle.SetTextFont(font)
	ROOT.gStyle.SetStatFont(font)
	ROOT.gStyle.SetStatFontSize(0.05)
	ROOT.gStyle.SetStatX(0.97)
	ROOT.gStyle.SetStatY(0.98)
	ROOT.gStyle.SetStatH(0.03)
	ROOT.gStyle.SetStatW(0.3)
	ROOT.gStyle.SetTickLength(0.02, "y")
	ROOT.gStyle.SetEndErrorSize(3)
	ROOT.gStyle.SetLabelSize(0.05, "xyz")
	ROOT.gStyle.SetLabelFont(font, "xyz")
	ROOT.gStyle.SetLabelOffset(0.01, "xyz")
	ROOT.gStyle.SetTitleFont(font, "xyz")
	ROOT.gStyle.SetTitleOffset(1.1, "xy")
	ROOT.gStyle.SetTitleSize(0.05, "xyz")
	ROOT.gStyle.SetMarkerSize(1.3)
	# ROOT.gStyle.SetPalette(1, 0)

	ROOT.gROOT.ForceStyle()
	ROOT.gStyle.SetOptStat(0)
	ROOT.gStyle.SetOptTitle(0)
	ROOT.gStyle.SetLineWidth(2)
	ROOT.gStyle.SetLegendFont(42)
	ROOT.gStyle.SetLegendBorderSize(0)
	ROOT.gStyle.SetLegendFillColor(10)
	ROOT.gStyle.SetPadTickY(1)
	ROOT.gStyle.SetPadTickX(1)
	ROOT.gStyle.SetEndErrorSize(0)

	canvas.SetFillColor(0)
	canvas.SetBorderMode(0)
	canvas.SetBorderSize(0)
	canvas.SetLeftMargin(0.18)
	canvas.SetRightMargin(0.1)
	canvas.SetBottomMargin(0.1518219)
	canvas.SetTopMargin(0.)
	canvas.SetFrameBorderMode(0)

# =============================================================================
# The END
# =============================================================================
