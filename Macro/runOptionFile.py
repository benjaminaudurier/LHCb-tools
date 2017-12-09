import os

# ======== define variables ========
DaVinciVersion = 'v42r6p1'
optionsFile = 'option_very-low-pt-excess.py'
data = '../../datasets/validation_Lead15_Beam6370GeV-VeloClosed-MagDown_RealData_Reco15aLead15_Stripping31_90000000_IFT_DST.py'
NofFilePerJob = 3
# ========

# ======== set job ========
j = Job(name='Analysis')
if os.path.isdir("./DaVinciDev_{}".format(DaVinciVersion)) is True:
	j.application = GaudiExec()
	j.application.directory = "./DaVinciDev_{}".format(DaVinciVersion)
else:
	j.application = prepareGaudiExec('DaVinci', DaVinciVersion, myPath='.')

j.application.options = [optionsFile]
j.application.readInputData(data)
j.backend = Dirac()
j.outputfiles = [DiracFile('*.root'), LocalFile('stdout')]
# j.outputfiles = [LocalFile('*.root')]
j.splitter = SplitByFiles(filesPerJob=NofFilePerJob)
j.submit()
#========
