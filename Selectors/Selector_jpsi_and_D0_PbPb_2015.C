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

   TNtuple *nt = new TNtuple("nt","nt","Jpsi_MM:Jpsi_PT:Jpsi_Y:Jpsi_OWNPV_Z:DV:dZ:tZ:Hcal:Ecal:nVeloClusters");
   GetOutputList()->Add(nt);

   // Control Histio
   TH1F *hruns = new TH1F("hruns","runs",169618-168487,168487,169618);
   GetOutputList()->Add(hruns);

   TH1F *hexEvent = new TH1F("hexEvent","runs",169618-168487,168487,169618);
   GetOutputList()->Add(hexEvent);


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
   //if(static_cast<int>(entry)%10000 == 0)
      //printf("Proccess event %d \n", static_cast<int>(entry));


   // Get object to fill
   TNtuple *nt  = static_cast<TNtuple*>(GetOutputList()->FindObject("nt"));
   TH1F *hruns  = static_cast<TH1F*>(GetOutputList()->FindObject("hruns"));
   TH1F *hexEvent  = static_cast<TH1F*>(GetOutputList()->FindObject("hexEvent"));


   // for cross checks
   hruns->Fill( *runNumber );

   // Check the event candidates
   if ( ! IsEventSelected() ) {

	  hexEvent->Fill( *runNumber );
	  return kFALSE;
   }

   // if ( hasGhosts() ) return kFALSE;

   // Prepare data
   TVector3 v_OWNPV( *Jpsi_OWNPV_X, *Jpsi_OWNPV_Y, *Jpsi_OWNPV_Z);
   TVector3 v_ENDVERTEX(*Jpsi_ENDVERTEX_X, *Jpsi_ENDVERTEX_Y, *Jpsi_ENDVERTEX_Z);

   Double_t OWNPV_R = v_OWNPV.Perp();
   Double_t ENDVERTEX_R = v_ENDVERTEX.Perp();

   v_OWNPV -= v_ENDVERTEX;

   Double_t dZ = (*Jpsi_ENDVERTEX_Z - *Jpsi_OWNPV_Z)*1e-3; // in metres
   Double_t tZ = dZ * 3096.916/(*Jpsi_PZ * TMath::C());

   nt->Fill( *Jpsi_MM, *Jpsi_PT, *Jpsi_Y, *Jpsi_OWNPV_Z, v_OWNPV.Mag(), dZ, tZ, *eHcal, *eEcal, static_cast<Double_t>(*nVeloClusters) );

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
   TH1F *hexEvent  = static_cast<TH1F*>(GetOutputList()->FindObject("hexEvent"));

   // save results
   TFile outputfile("Selector_jpsi_and_D0_PbPb_2015.root","recreate");
   nt->Write();
   hruns->Write();
   hexEvent->Write();

   outputfile.Close();
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

      temp_mup->SetPxPyPzE(*muplus_PX, *muplus_PY, *muplus_PZ, *muplus_PE);
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
bool Selector_jpsi_and_D0_PbPb_2015::IsEventSelected()
{
   // This function may be called from Loop.
   // returns  1 if entry is accepted.
   // returns -1 otherwise.

   // ------------------------------------------
   //  Luminosity cut
   // ------------------------------------------
   if( *nPVs < 1 ) return kFALSE;

   if( *Jpsi_OWNPV_Z < -200. || *Jpsi_OWNPV_Z > 200. ) return kFALSE;
   if( *Jpsi_ENDVERTEX_Z < -200. || *Jpsi_ENDVERTEX_Z > 200. ) return kFALSE;

   // create vectors of the vertices
   TVector3 v_OWNPV(*Jpsi_OWNPV_X,*Jpsi_OWNPV_Y,*Jpsi_OWNPV_Z);
   TVector3 v_ENDVERTEX(*Jpsi_ENDVERTEX_X,*Jpsi_ENDVERTEX_Y,*Jpsi_ENDVERTEX_Z);

   Double_t OWNPV_R = v_OWNPV.Perp();
   Double_t ENDVERTEX_R = v_ENDVERTEX.Perp();

   if( OWNPV_R < 0.35 || OWNPV_R > 0.95 ) return kFALSE;
   if( ENDVERTEX_R < 0.35 || ENDVERTEX_R > 0.95 ) return kFALSE;

   // ------------------------------------------
   //  Jpsi selection
   // ------------------------------------------

   // muon dynamical cuts
   if ( *muplus_PT < 750. || *muminus_PT< 750. ) return kFALSE;

   // goodness of the muon track
   if ( *muplus_TRACK_GhostProb  > 0.5 || *muminus_TRACK_GhostProb > 0.5 ) return kFALSE;
   if ( *muplus_ProbNNghost > 0.8 || *muminus_ProbNNghost > 0.8 ) return kFALSE;
   if ( *muplus_TRACK_CHI2NDOF > 3. || *muminus_TRACK_CHI2NDOF > 3. )  return kFALSE;

   // muon track close to the vertex
   if ( *muplus_IP_OWNPV > 3. || *muminus_IP_OWNPV > 3. ) return kFALSE;

   // muon id
   if ( *muplus_PIDmu <  3. || *muminus_PIDmu < 3. ) return kFALSE;
   // if ( *muplus_PIDK >  6. || *muminus_PIDK > 6. ) return kFALSE;

   // Jpsi cuts
   // if ( *Jpsi_MM < 2900. || *Jpsi_MM > 3200. ) return kFALSE;
   if ( TMath::Prob(*Jpsi_ENDVERTEX_CHI2, *Jpsi_ENDVERTEX_NDOF) < 0.5/100.0 ) return kFALSE;

   return kTRUE;
}
