#define Selector_jpsi_and_D0_PbPb_2015_cxx
// The class definition in Selector_jpsi_and_D0_PbPb_2015.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.


// The following methods are defined in this file:
//    Begin():        called every time a loop on the tree starts,
//                    a convenient place to create your histograms.
//    SlaveBegin():   called after Begin(), when on PROOF called only on the
//                    slave servers.
//    Process():      called for each event, in this function you decide what
//                    to read and fill your histograms.
//    SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//                    called only on the slave servers.
//    Terminate():    called at the end of the loop on the tree,
//                    a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// root> T->Process("Selector_jpsi_and_D0_PbPb_2015.C")
// root> T->Process("Selector_jpsi_and_D0_PbPb_2015.C","some options")
// root> T->Process("Selector_jpsi_and_D0_PbPb_2015.C+")
//


#include "Selector_jpsi_and_D0_PbPb_2015.h"
#include <TH2.h>
#include <TStyle.h>
#include <TNtuple.h>
#include <TObjArray.h>
#include <THnSparse.h>
#include <TMath.h>
#include <TVector3.h>
#include <TLorentzVector.h>

// ______________________________________________________
void Selector_jpsi_and_D0_PbPb_2015::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
}

// ______________________________________________________
void Selector_jpsi_and_D0_PbPb_2015::SlaveBegin(TTree * /*tree*/)
{
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();

   // Bin definitions for the THnSparse
   Int_t nBins_MM       = 50;
   Double_t MM_low_edge = 2900.;
   Double_t MM_up_edge  = 3300.;

   Int_t nBins_PT        = 100;
   Double_t PT_low_edge = 0.;
   Double_t PT_up_edge  = 10000.;

   Int_t nBins_Y       = 2;
   Double_t Y_low_edge = 2.;
   Double_t Y_up_edge  = 4.5;

   Int_t nBins_OWNPV_Z        = 500;
   Double_t OWNPV_Z_low_edge = -1000.;
   Double_t OWNPV_Z_up_edge  =  1000.;

   Int_t nBins_ENDVERTEX_Z        = 500;
   Double_t ENDVERTEX_Z_low_edge = -1000.;
   Double_t ENDVERTEX_Z_up_edge  =  1000.;

   Int_t nBins_DistV        = 200;
   Double_t DistV_low_edge =  0.;
   Double_t DistV_up_edge  =   10.;

   Int_t nBins_dZ        = 200;
   Double_t dZ_low_edge =  -10.;
   Double_t dZ_up_edge  =   10.;

   Int_t nBins_tZ        = 400;
   Double_t tZ_low_edge =  -20.;
   Double_t tZ_up_edge  =   20.;

   Int_t nBins_MuPlus_PIDmu        = 500;
   Double_t MuPlus_PIDmu_low_edge = -30.;
   Double_t MuPlus_PIDmu_up_edge  =  30.;

   Int_t nBins_MuMinus_PIDmu        = 500;
   Double_t MuMinus_PIDmu_low_edge = -30.;
   Double_t MuMinus_PIDmu_up_edge  =  30.;

   Int_t nBins_MuPlus_PIDK        = 500;
   Double_t MuPlus_PIDK_low_edge = -30.;
   Double_t MuPlus_PIDK_up_edge  =  30.;

   Int_t nBins_MuMinus_PIDK        = 500;
   Double_t MuMinus_PIDK_low_edge = -30.;
   Double_t MuMinus_PIDK_up_edge  =  30.;

   Int_t nBins_eHcal        =  500;
   Double_t eHcal_low_edge =   0.;
   Double_t eHcal_up_edge  =  1.1e7;

   Int_t nBins_eEcal        =  500;
   Double_t eEcal_low_edge =   0.;
   Double_t eEcal_up_edge  =   1.1e7;

   Int_t nBins_nVeloClusters        = 200;
   Double_t nVeloClusters_low_edge =   0.;
   Double_t nVeloClusters_up_edge  =   20000.;

   enum {
      kMMaxis,
      kPTaxis,
      kYaxis,
      kZaxis,
      kDistVaxis,
      kdZaxis,
      ktZaxis,
      kMuPlusPIDmuaxis,
      kMuMinusPIDmuaxis,
      kMuPlusPIDKaxis,
      kMuMinusPIDKaxis,
      keHcal,
      keEcal,
      kVeloClusters,
      kNaxis};

   TNtuple *nt = new TNtuple("nt","nt","MM:PT:Y:Z:DV:dZ:tZ:plusPIDmu:minusPIDmu:plusPIDK:minusPIDK:Hcal:Ecal:Velo");
   GetOutputList()->Add(nt);

   Int_t bins[]     = {
      nBins_MM,
      nBins_PT,
      nBins_Y,
      nBins_OWNPV_Z,
      nBins_DistV,
      nBins_dZ,
      nBins_tZ,
      nBins_MuPlus_PIDmu,
      nBins_MuMinus_PIDmu,
      nBins_MuPlus_PIDK,
      nBins_MuMinus_PIDK,
      nBins_eHcal,
      nBins_eEcal,
      nBins_nVeloClusters};
   Double_t lbins[] = {
      MM_low_edge,
      PT_low_edge,
      Y_low_edge,
      OWNPV_Z_low_edge,
      DistV_low_edge,
      dZ_low_edge,
      tZ_low_edge,
      MuPlus_PIDmu_low_edge,
      MuMinus_PIDmu_low_edge,
      MuPlus_PIDK_low_edge,
      MuMinus_PIDK_low_edge,
      eHcal_low_edge,
      eEcal_low_edge,
      nVeloClusters_low_edge};
   Double_t hbins[] = {
      MM_up_edge,
      PT_up_edge,
      Y_up_edge,
      OWNPV_Z_up_edge,
      DistV_up_edge,
      dZ_up_edge,
      tZ_up_edge,
      MuPlus_PIDmu_up_edge,
      MuMinus_PIDmu_up_edge,
      MuPlus_PIDK_up_edge,
      MuMinus_PIDK_up_edge,
      eHcal_up_edge,
      eEcal_up_edge,
      nVeloClusters_up_edge};

   THnSparseD *hn = new THnSparseD("hSparse","hSparse", kNaxis, bins, lbins, hbins );
   hn->GetAxis( kMMaxis )->SetTitle( "MM( #mu^{+}#mu^{-}) [MeV/c^{2}]" );
   hn->GetAxis( kPTaxis )->SetTitle( "p_{T}( #mu^{+}#mu^{-}) [MeV/c]" );
   hn->GetAxis( kYaxis )->SetTitle( "rapidity ( #mu^{+}#mu^{-})" );
   hn->GetAxis( kZaxis )->SetTitle( "OWNPV_Z [mm]" );
   hn->GetAxis( kDistVaxis )->SetTitle( "Delta(OWNPV-ENDVERTEX) [mm]" );
   hn->GetAxis( kMuPlusPIDmuaxis )->SetTitle( "MuPlus PIDmu" );
   hn->GetAxis( kMuMinusPIDmuaxis )->SetTitle( "MuMinus PIDmu" );
   hn->GetAxis( kMuPlusPIDKaxis )->SetTitle( "MuPlus PIDK" );
   hn->GetAxis( kMuMinusPIDKaxis )->SetTitle( "MuMinus PIDK" );
   hn->GetAxis( keHcal )->SetTitle("eHcal [MeV]" );
   hn->GetAxis( keEcal )->SetTitle("eEcal [MeV]" );
   hn->GetAxis( kVeloClusters )->SetTitle( "nVeloClusters" );
   GetOutputList()->Add(hn);

   // Control Histio
   TH1F *hruns = new TH1F("hruns","runs",169618-168487,168487,169618);
   GetOutputList()->Add(hruns);

   // Used in hasGhosts
   TObjArray* mup = new TObjArray();
   mup->SetName("mup");
   TObjArray* mum = new TObjArray();
   mum->SetName("mum");
   GetOutputList()->Add(mup);
   GetOutputList()->Add(mum);

}

// ______________________________________________________
Bool_t Selector_jpsi_and_D0_PbPb_2015::Process(Long64_t entry)
{
   // The Process() function is called for each entry in the tree (or possibly
   // keyed object in the case of PROOF) to be processed. The entry argument
   // specifies which entry in the currently loaded tree is to be processed.
   // When processing keyed objects with PROOF, the object is already loaded
   // and is available via the fObject pointer.
   //
   // This function should contain the \"body\" of the analysis. It can contain
   // simple or elaborate selection criteria, run algorithms on the data
   // of the event and typically fill histograms.
   //
   // The processing can be stopped by calling Abort().
   //
   // Use fStatus to set the return value of TTree::Process().
   //
   // The return value is currently not used.

   fReader.SetLocalEntry(entry);

   // print progress
   if(static_cast<int>(entry)%10000 == 0)
      printf("Proccess event %d \n", static_cast<int>(entry));


   // Get object to fill
   TNtuple *nt  = static_cast<TNtuple*>(GetOutputList()->FindObject("nt"));
   TH1F *hruns  = static_cast<TH1F*>(GetOutputList()->FindObject("hruns"));
   THnSparseD *hsparse = static_cast<THnSparseD*>(GetOutputList()->FindObject("hSparse"));

   // for cross checks
   hruns->Fill( *runNumber );

   // Check the event candidates
   if ( IsEventSelected() < 1 ) return kFALSE;
   if ( hasGhosts() ) return kFALSE;

   // Prepare data
   TVector3 v_OWNPV( *Jpsi_OWNPV_X, *Jpsi_OWNPV_Y, *Jpsi_OWNPV_Z);
   TVector3 v_ENDVERTEX(*Jpsi_ENDVERTEX_X, *Jpsi_ENDVERTEX_Y, *Jpsi_ENDVERTEX_Z);

   Double_t OWNPV_R = v_OWNPV.Perp();
   Double_t ENDVERTEX_R = v_ENDVERTEX.Perp();

   v_OWNPV -= v_ENDVERTEX;

   Double_t dZ = (*Jpsi_ENDVERTEX_Z - *Jpsi_OWNPV_Z)*1e-3; // in metres
   Double_t tZ = dZ * 3096.916/(*Jpsi_PZ * TMath::C());

   // Fill object
   Double_t data[] = {
      *Jpsi_MM,
      *Jpsi_PT,
      *Jpsi_Y,
      *Jpsi_OWNPV_Z,
      v_OWNPV.Mag(),
      dZ,
      tZ,
      *muplus_PIDmu,
      *muminus_PIDmu,
      *muplus_PIDK,
      *muminus_PIDK,
      *eHcal,
      *eEcal,
      static_cast<Double_t>(*nVeloClusters)
    };
  hsparse->Fill(data);

  int N = sizeof(data)/sizeof(data[0]);
  Float_t *dataF = new Float_t[N];
  for( int i=0;i<N;i++) dataF[i] = data[i];
  nt->Fill( dataF );
  delete[] dataF;

   return kTRUE;
}

// ______________________________________________________
void Selector_jpsi_and_D0_PbPb_2015::SlaveTerminate()
{
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.

}


// ______________________________________________________
void Selector_jpsi_and_D0_PbPb_2015::Terminate()
{
   // The Terminate() function is the last function to be called during
   // a query. It always runs on the client, it can be used to present
   // the results graphically or save the results to file.

   // Get the output object
   TNtuple *nt  = static_cast<TNtuple*>(GetOutputList()->FindObject("nt"));
   TH1F *hruns  = static_cast<TH1F*>(GetOutputList()->FindObject("hruns"));
   THnSparseD *hsparse = static_cast<THnSparseD*>(GetOutputList()->FindObject("hSparse"));


   // save results
   TFile outputfile("Selector_jpsi_and_D0_PbPb_2015.root","recreate");
   nt->Write();
   hruns->Write();
   hsparse->Write();

   outputfile.Close();

   // if ( GetOutputList()->FindObject("mum") ) delete GetOutputList()->FindObject("mum") ;
   // if ( GetOutputList()->FindObject("mup") ) delete GetOutputList()->FindObject("mup") ;

}


// ______________________________________________________
bool Selector_jpsi_and_D0_PbPb_2015::hasGhosts()
{
   // check if a candidate is formed by muons extremely close to previous candidates

   TLorentzVector *temp_mum = new TLorentzVector();
   TLorentzVector *temp_mup = new TLorentzVector();

   TObjArray* mum = static_cast<TObjArray*>(GetOutputList()->FindObject("mum"));
   TObjArray* mup = static_cast<TObjArray*>(GetOutputList()->FindObject("mup"));

   if( mum->GetEntriesFast() == 0 ) {

      temp_mum->SetPxPyPzE(*muplus_PX, *muplus_PY, *muplus_PZ, *muplus_PE);
      temp_mup->SetPxPyPzE(*muminus_PX, *muminus_PY, *muminus_PZ, *muminus_PE);
      mum->Add(temp_mum);
      mup->Add(temp_mup);
      delete temp_mum;
      delete temp_mup;
      return kFALSE;

   } else {

      double deltaThetaMuP = -999.0;
      double deltaThetaMuM = -999.0;

      temp_mum->SetPx( *muplus_PX);
      temp_mum->SetPy( *muplus_PY);
      temp_mum->SetPz( *muplus_PZ);
      temp_mum->SetE(  *muplus_PE);
      temp_mup->SetPxPyPzE(*muminus_PX, *muminus_PY, *muminus_PZ, *muminus_PE);

      for(int icand=0; icand < mum->GetEntriesFast(); icand++) {
         deltaThetaMuM = static_cast<TLorentzVector*>(mum->At(icand))->Angle(temp_mum->Vect());
         for(int jcand=0; jcand < mup->GetEntriesFast(); jcand++) {
            deltaThetaMuP = static_cast<TLorentzVector*>(mup->At(jcand))->Angle(temp_mup->Vect());
            if(cos(deltaThetaMuP)>0.9999 && cos(deltaThetaMuM)>0.9999) return kTRUE;
         }
      }
      mum->Add(temp_mum);
      mup->Add(temp_mup);
      delete temp_mum;
      delete temp_mup;
      return kFALSE;
   }

   delete temp_mum;
   delete temp_mup;
   return kFALSE;
}

// ______________________________________________________
Int_t Selector_jpsi_and_D0_PbPb_2015::IsEventSelected()
{
   // This function may be called from Loop.
   // returns  1 if entry is accepted.
   // returns -1 otherwise.

   // ------------------------------------------
   //  Luminosity cut
   // ------------------------------------------
   if( *nPVs < 1 ) return -1;

   if( ! (*Jpsi_OWNPV_Z > -200. && *Jpsi_OWNPV_Z < 200. ) ) return -1;
   if( ! (*Jpsi_ENDVERTEX_Z > -200. && *Jpsi_ENDVERTEX_Z < 200. ) ) return -1;

   // create vectors of the vertices
   TVector3 v_OWNPV(*Jpsi_OWNPV_X,*Jpsi_OWNPV_Y,*Jpsi_OWNPV_Z);
   TVector3 v_ENDVERTEX(*Jpsi_ENDVERTEX_X,*Jpsi_ENDVERTEX_Y,*Jpsi_ENDVERTEX_Z);

   Double_t OWNPV_R = v_OWNPV.Perp();
   Double_t ENDVERTEX_R = v_ENDVERTEX.Perp();

   if( ! ( OWNPV_R > 0.35 && OWNPV_R < 0.95 ) ) return -1;
   if( ! ( ENDVERTEX_R > 0.35 && ENDVERTEX_R < 0.95 ) ) return -1;

   // ------------------------------------------
   //  Jpsi selection
   // ------------------------------------------

   if (!(*muplus_PT>750. && *muminus_PT>750.)) return -1;

   if ( *muplus_TRACK_GhostProb  > 0.5) return -1;
   if ( *muminus_TRACK_GhostProb > 0.5) return -1;

   if ( *muplus_ProbNNghost  > 0.8) return -1;
   if ( *muminus_ProbNNghost  > 0.8) return -1;

   // goodness of the muon track
   if ( *muplus_TRACK_CHI2NDOF > 3. )  return -1;
   if ( *muminus_TRACK_CHI2NDOF > 3. ) return -1;

   // muon track close to the vertex
   if ( *muplus_IP_OWNPV > 3. ) return -1;
   if ( *muminus_IP_OWNPV > 3. ) return -1;

   // muon id
   if ( *muplus_PIDmu <  3. ) return -1;
   if ( *muminus_PIDmu < 3. ) return -1;

   //if ( *muplus_PIDK >  6. ) return -1;
   //if ( *muminus_PIDK > 6. ) return -1;

   // goodness of the dimuon vertex
   if ( TMath::Prob(*Jpsi_ENDVERTEX_CHI2, *Jpsi_ENDVERTEX_NDOF) < 0.5/100.0 ) return -1;


   return 1;
}