void combinedplot(){
  TFile* File1 = new TFile("/afs/cern.ch/work/n/nsolomon/FCC/WorkDir/OutDir/ZH/heppy.analyzers.examples.zh_had.TreeProducer.TreeProducer_1/tree.root","READ");
  THStack *hs = new THStack("hs","Di-photon invariant mass;Higgs mass (GeV);Events/Gev");

 TH1F *h1 = new TH1F("h1", "Higgs mass", 30, 110, 140);
 TTreeReader reader1("events",File1);
 TTreeReaderValue<double>hmass1(reader1,"higgs_m");

 
 while(reader1.Next()){
 h1->Fill(*hmass1);
 }
 Double_t scale1 =0.4614*500/10000;
 h1->Scale(scale1);
 h1->SetFillColor(kRed);

 TFile* File2 = new TFile("/afs/cern.ch/work/n/nsolomon/FCC/WorkDir/OutDir/Bkg/heppy.analyzers.examples.zh_had.TreeProducer.TreeProducer_1/tree.root","READ");
 TH1F *h2 = new TH1F("h2", "Higgs mass", 30, 110, 140);
 TTreeReader reader2("events",File2);
 TTreeReaderValue<double>hmass2(reader2,"higgs_m");


 while(reader2.Next()){
   h2->Fill(*hmass2);
 }
 Double_t scale2 = 78780*500/5000000; 
 h2->Scale(scale2);
 h2->SetFillColor(kBlue);
 hs->Add(h2); 
 hs->Add(h1);
 

 hs->Draw("HIST");

 TH1F *h3 = new TH1F("h3", "Higgs mass", 30, 110, 140);
 h3->Add(h2);
 h3->Add(h1);

 TF1* fit = new TF1("fit", "gaus", 110, 140);
 h3->Fit("fit");
 fit->SetLineColor(kRed+1);

 TF1* bkg_fit = new TF1("bkg_fit", "pol 3", 110, 140);
 h2->Fit("bkg_fit");
 bkg_fit->SetLineColor(kBlack);
 
 hs->Draw("hist");
 //fit->Draw("func same");
 bkg_fit->Draw("func same");

}
