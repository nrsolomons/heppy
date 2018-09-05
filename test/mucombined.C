TH1F* histbkg(string cuts="",string var="mjj"){
    string ges="/afs/cern.ch/work/n/nsolomon/FCC/WorkDir/Mumu/Bkg/heppy.analyzers.examples.zh_had.TreeProducer_mu.TreeProducer_1/tree.root";
    TFile *file=new TFile(ges.c_str());
    TTree *eventsWW;
    file->GetObject("events", eventsWW);
    eventsWW->Draw((var+">>+htemp(12,114,138)").c_str(),cuts.c_str());
    TH1F *ph = (TH1F*) file->Get("htemp");
    gPad->GetListOfPrimitives()->Remove(ph);
    ph->SetDirectory(0);
    file->Close(); 
    return ph;
}

TH1F* histsig(string cuts="",string var="mjj"){
    string ges="/afs/cern.ch/work/n/nsolomon/FCC/WorkDir/Mumu/ZH/heppy.analyzers.examples.zh_had.TreeProducer_mu.TreeProducer_1/tree.root";
    TFile *file=new TFile(ges.c_str());
    TTree *eventsWW;
    file->GetObject("events", eventsWW);
    eventsWW->Draw((var+">>+htemp(12,114,138)").c_str(),cuts.c_str());
    TH1F *ph = (TH1F*) file->Get("htemp");
    gPad->GetListOfPrimitives()->Remove(ph);
    ph->SetDirectory(0);
    file->Close(); 
    return ph;
}
void mucombined(){

  auto c=new TCanvas("Canvas","Canvas",1200,800);
gStyle->SetOptStat(0);


THStack *hs = new THStack("hs","Di-muon invariant mass;Higgs mass (GeV);Events/2Gev");

TH1F* h1=histsig("","higgs_m");
Double_t scale1=43.99*2./10000.;
h1->Scale(scale1);
h1->SetFillColor(kRed+1);
h1->SetFillStyle(3144);
TH1F* h2=histbkg("","higgs_m");
Double_t scale2=1300.*2000./5000000.;
h2->Scale(scale2);
h2->SetFillColor(kBlue);
h2->SetFillStyle(3244);
hs->Add(h2);
hs->Add(h1);
TH1F *h3=new TH1F("h3","Higgs mass",12,114,138);
h3->Add(h1);
h3->Add(h2);

//TF1* fit1 = new TF1("fit1", "gaus", 114, 138);
//h1->Fit("fit1");
//Double_t integral1 = fit1->Integral(114, 138);
//cout << "Signal integral = " << integral1 << endl;
//Double_t chi21 = h1->GetFunction("fit1")->GetChisquare();
//cout << "Signal chi2 = " << chi21 << endl;
//TF1 *f = (TF1*)fit1->Clone("f");
//
//TF1* fit2 = new TF1("fit2", "pol3", 114, 138);
//h2->Fit("fit2");
//Double_t integral2 = fit2->Integral(114, 138);
//cout << "Background integral = " << integral2 << endl;
//Double_t chi22= h2->GetFunction("fit2")->GetChisquare();
//cout << "Background chi2 = " << chi22 << endl;
//TF1 *g = (TF1*)fit2->Clone("g");
//
//TF1* fit3 = new TF1("fit3", "f+g");
//h3->Fit("fit3");

hs->Draw("hist");
//h3->Draw("same func");
hs->SetMinimum(100);
hs->SetMaximum(330);

auto legend = new TLegend(0.9,0.3,0.5,0.1);
legend->AddEntry(h1,"Signal events","f");
legend->AddEntry(h2,"Background events","f");
//legend->AddEntry(fit3,"Fit","l");
legend->Draw("same");

}

