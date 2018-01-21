{
	gROOT->ProcessLine(".L filter_jpsi_and_D0_PbPb_2015_wn.C");
    gROOT->ProcessLine("filter_jpsi_and_D0_PbPb_2015_wn t");
    gROOT->ProcessLine("t.Loop()");
}
