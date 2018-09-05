from heppy.framework.analyzer import Analyzer
from heppy.analyzers.IsolationAnalyzer import IsolationAnalyzer
from heppy.utils.deltar import deltaR
from heppy.particles.isolation import EtaPhiCircle
from heppy.statistics.counter import Counter
from itertools import combinations
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from heppy.particles.jet import JetConstituents
from heppy.particles.jet import JetComponent
import heppy.framework.config as cfg

import math
import numpy
class Selection2(Analyzer):

    def beginLoop(self, setup):
        super(Selection2, self).beginLoop(setup)
        self.counters.addCounter('cut_flow') 
        self.counters['cut_flow'].register('All events')
        self.counters['cut_flow'].register('EM fraction < 0.8')
    
    def process(self, event):

        self.counters['cut_flow'].inc('All events')
        newparticles = getattr(event, self.cfg_ana.newparticles)
        higgscandidates = getattr(event, self.cfg_ana.higgscandidates)
        jets = getattr(event, self.cfg_ana.input_jets)
        emfrac = [0,0]
        for i in range(len(jets)):
            emfrac[i] = (jets[i].constituents[22].e()+jets[i].constituents[11].e())/jets[i].e() 
    	if emfrac[0]>0.8 and emfrac[1]>0.8:
            return False 
        self.counters['cut_flow'].inc('EM fraction < 0.8')

        higgs = Resonance(higgscandidates[0], higgscandidates[1], 25)
        setattr(event, self.cfg_ana.higgs, higgs)
