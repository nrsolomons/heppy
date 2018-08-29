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
        particles = getattr(event, self.cfg_ana.particles)
        higgscandidates = getattr(event, self.cfg_ana.higgscandidates)
	jets = getattr(event, self.cfg_ana.input_jets)
#	for particle in particles:
#	    if particle.pdgid() in [11,-11]:
#		print 'oh no!'
#		print particle.e()
	notphoton = []
	for jet in jets:
	    emfrac = (jet.constituents[211].e() +jet.constituents[11].e()+jet.constituents[22].e())/jet.e()
	    if emfrac < 0.8:
		notphoton.append(jet)
	if len(notphoton)<1:
	    return False 
        self.counters['cut_flow'].inc('EM fraction < 0.8')

	higgs = Resonance(higgscandidates[0], higgscandidates[1], 25)
	setattr(event, self.cfg_ana.higgs, higgs)
