from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter

import math
import numpy
class Selection(Analyzer):

    def beginLoop(self, setup):
        super(Selection, self).beginLoop(setup)
        self.counters.addCounter('cut_flow') 
        self.counters['cut_flow'].register('All events')
        self.counters['cut_flow'].register('No lepton')
        self.counters['cut_flow'].register('4 jets')
        self.counters['cut_flow'].register('4 jets with E>15')
        self.counters['cut_flow'].register('2 b jets')
    
    def process(self, event):



        self.counters['cut_flow'].inc('All events')
        if len(event.sel_iso_leptons) > 0:
            return True # could return False to stop processing
        self.counters['cut_flow'].inc('No lepton')
        jets = getattr(event, self.cfg_ana.input_jets)        
        if len(jets) < 4:
            return True
        self.counters['cut_flow'].inc('4 jets')
        if min(jet.e() for jet in jets) >= 15.:
            self.counters['cut_flow'].inc('4 jets with E>15')
        bjets = [jet for jet in jets if jet.tags['b']]
        if len(bjets) >= 2:
            self.counters['cut_flow'].inc('2 b jets')
        
        #find 2 highest energy photons

        gammas = getattr(event, self.cfg_ana.photons)
        print 'number of photons '
        print len(gammas)
        print gammas[0].e()
        photon_energies = (gamma.e() for gamma in gammas)
        mass = math.sqrt(2*(gammas[0].e()*gammas[1].e()) - 2*numpy.dot(gammas[0].p3(),gammas[1].p3()))

        #plus scalar prod of momenta
        
        print mass
        print (gammas[0]._tlv+gammas[1]._tlv).M()
