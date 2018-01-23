from Ostap.Data import Data

# =============================================================================
if __name__ == '__main__':

    # patterns = '/eos/lhcb/user/b/baudurie/ntuple_jpsi_and_D0_PbPb_2015/jpsi_and_D0_PbPb_2015/*/*/output/PbPb_D0_Jpsi.root'
    # patterns = '/eos/lhcb/user/b/baudurie/ntuple_jpsi_and_D0_PbPb_2015/jpsi_and_D0_PbPb_2015/229/*/output/PbPb_D0_Jpsi.root'
    #
    patterns = '/st100-gr1/audurier/ntuple_jpsi_and_D0_PbPb_2015/jpsi_and_D0_PbPb_2015/*/*/output/PbPb_D0_Jpsi.root'
    # patterns = '/st100-gr1/audurier/ntuple_jpsi_and_D0_PbPb_2015/jpsi_and_D0_PbPb_2015/229/*/output/PbPb_D0_Jpsi.root'

    chain = Data('Jpsi/DecayTree', patterns).chain
    # chain.Process("/afs/cern.ch/user/b/baudurie/public/LHCb-tools/Filter_jpsi_PbPb_2015_lxplus.C+")
    # chain.Process("/afs/cern.ch/user/b/baudurie/public/LHCb-tools/Selectors/Selector_jpsi_and_D0_PbPb_2015.C+")
    chain.Process("/home/audurier/LHCb-tools/Selectors/Selector_jpsi_and_D0_PbPb_2015.C+")
