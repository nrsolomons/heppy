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
        self.taggers = 'gamma' 
        bookParticle(self.tree, 'higgs')
        bookParticle(self.tree, 'photon1')
        bookParticle(self.tree, 'photon2')
        bookParticle(self.tree, 'matchedphoton1')
        bookParticle(self.tree, 'matchedphoton2')
        bookParticle(self.tree, 'mother1')
        bookParticle(self.tree, 'mother2')
        var(self.tree, 'status1')
        var(self.tree, 'status2')
        var(self.tree, 'isolation1')
        var(self.tree, 'isolation2')
        var(self.tree, 'etagap')
        var(self.tree, 'isosum') 
       
    def process(self, event):
        self.tree.reset()

        higgs = getattr(event, self.cfg_ana.higgs)
        if higgs:
            fillParticle(self.tree, 'higgs', higgs)
        photons = getattr(event, self.cfg_ana.photons)
        for i, photon in enumerate(reversed(photons)):
            if i == 2:
                break
            fillParticle(self.tree,
                       'photon{i}'.format(i=i+1), 
                       photon)

        matchedphotons = getattr(event, self.cfg_ana.matchedphotons)
        for i, matchedphoton in enumerate(reversed(matchedphotons)):
            if i == 2:
                break
            fillParticle(self.tree,
                       'matchedphoton{i}'.format(i=i+1), 
                       matchedphoton)
        
        mothers = getattr(event, self.cfg_ana.mothers)
        for i, mother in enumerate(mothers):
            if i == 2:
                break
            if mother is None:
                break
            fillParticle(self.tree,
                       'mother{i}'.format(i=i+1), 
                       mother)
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
