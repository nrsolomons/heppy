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
        self.taggers = 'mu'
        bookParticle(self.tree, 'higgs')
        bookParticle(self.tree, 'muon1')
        bookParticle(self.tree, 'muon2')
        var(self.tree, 'lenmu') 
       
    def process(self, event):
        self.tree.reset()

        lenmu=getattr(event, self.cfg_ana.lenmu)
        fill(self.tree, 'lenmu',lenmu)

        higgs = getattr(event, self.cfg_ana.higgs)
        if higgs:
            fillParticle(self.tree, 'higgs', higgs)
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
