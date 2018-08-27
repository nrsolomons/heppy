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
        self.taggers = 'gamma' #is this right?
        #bookJet(self.tree, 'jet1', self.taggers)
        #bookJet(self.tree, 'jet2', self.taggers)
        #bookJet(self.tree, 'jet3', self.taggers)
        #bookJet(self.tree, 'jet4', self.taggers)
        #bookParticle(self.tree, 'misenergy')
        bookParticle(self.tree, 'higgs')
        #bookParticle(self.tree, 'zed')
        bookParticle(self.tree, 'photon1')
        bookParticle(self.tree, 'photon2')
	var(self.tree, 'status1')
	var(self.tree, 'status2')
	var(self.tree, 'isolation1')
	var(self.tree, 'isolation2')
	var(self.tree, 'etagap')
	var(self.tree, 'isosum')
	
#	var(self.tree, 'h_mass')
        
       
    def process(self, event):
        self.tree.reset()

#        hmass=getattr(event, self.cfg_ana.hmass)
#	fill(self.tree,'h_mass',hmass)
        

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
        photons = getattr(event, self.cfg_ana.photons)
        for i, photon in enumerate(reversed(photons)):
            if i == 2:
                break
            fillParticle(self.tree,
                       'photon{i}'.format(i=i+1), 
                       photon)

        status = getattr(event, self.cfg_ana.status)
        for i, status in enumerate(reversed(status)):
            if i == 2:
                break
            fill(self.tree,
                       'status{i}'.format(i=i+1), 
                       status)
	
        isolations = getattr(event, self.cfg_ana.isolations)
        for i, isolation in enumerate(reversed(isolations)):
            if i == 2:
                break
            fill(self.tree,
                       'isolation{i}'.format(i=i+1), 
                       isolation)
	
        etagap=getattr(event, self.cfg_ana.etagap)
	fill(self.tree,'etagap',etagap)
       
        isosum=getattr(event, self.cfg_ana.isosum)
	fill(self.tree,'isosum',isosum)
	self.tree.tree.Fill()
         
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
