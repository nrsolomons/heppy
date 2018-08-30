from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *

from ROOT import TFile

class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        self.taggers = 'mu' #is this right?
        #bookJet(self.tree, 'jet1', self.taggers)
        #bookJet(self.tree, 'jet2', self.taggers)
        #bookJet(self.tree, 'jet3', self.taggers)
        #bookJet(self.tree, 'jet4', self.taggers)
        #bookParticle(self.tree, 'misenergy')
        bookParticle(self.tree, 'higgs')
        #bookParticle(self.tree, 'zed')
        bookParticle(self.tree, 'muon1')
        bookParticle(self.tree, 'muon2')
        var(self.tree, 'lenmu')
	var(self.tree, 'charged_hadron_e1')
	var(self.tree, 'muon_e1')
	var(self.tree, 'electron_e1')
	var(self.tree, 'photon_e1')
	
	var(self.tree, 'charged_hadron_e2')
	var(self.tree, 'muon_e2')
	var(self.tree, 'electron_e2')
	var(self.tree, 'photon_e2')
#	var(self.tree, 'h_mass')
        
       
    def process(self, event):
        self.tree.reset()

#        hmass=getattr(event, self.cfg_ana.hmass)
#	fill(self.tree,'h_mass',hmass)
        lenmu=getattr(event, self.cfg_ana.lenmu)
        fill(self.tree, 'lenmu',lenmu)

        charged_hadron_e=getattr(event, self.cfg_ana.charged_hadron_e)
        for i, charged_hadron_e in enumerate(reversed(charged_hadron_e)):
            if i == 2:
                break
            fill(self.tree,
                       'charged_hadron_e{i}'.format(i=i+1), 
			charged_hadron_e) 
        muon_e=getattr(event, self.cfg_ana.muon_e) 
        for i, muon_e in enumerate(reversed(muon_e)):
            if i == 2:
                break
            fill(self.tree,
                       'muon_e{i}'.format(i=i+1), 
			muon_e) 
        electron_e=getattr(event, self.cfg_ana.electron_e) 
        for i, electron_e in enumerate(reversed(electron_e)):
            if i == 2:
                break
            fill(self.tree,
                       'electron_e{i}'.format(i=i+1), 
			electron_e) 
        photon_e=getattr(event, self.cfg_ana.photon_e) 
        for i, photon_e in enumerate(reversed(photon_e)):
            if i == 2:
                break
            fill(self.tree,
                       'photon_e{i}'.format(i=i+1), 
			photon_e) 
        #misenergy = getattr(event, self.cfg_ana.misenergy)
        #fillParticle(self.tree, 'misenergy', misenergy )        
        #jets = getattr(event, self.cfg_ana.jets)
        #for ijet, jet in enumerate(jets):
        #    if ijet==4:
        #        break
        #    fillJet(self.tree, 'jet{ijet}'.format(ijet=ijet+1),
        #            jet, self.taggers)
        higgs = getattr(event, self.cfg_ana.higgs)
        if higgs:
            fillParticle(self.tree, 'higgs', higgs)
        #zed = getattr(event, self.cfg_ana.zed)
        #if zed:
        #    fillParticle(self.tree, 'zed', zed)
        muons = getattr(event, self.cfg_ana.muons)
        for i, muon in enumerate(reversed(muons)):
            if i == 2:
                break
            fillParticle(self.tree,
                       'muon{i}'.format(i=i+1), 
                       muon)
        self.tree.tree.Fill()
        
        
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
