from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter

import math
import numpy
class Selection(Analyzer):

    def beginLoop(self, setup):
        super(Selection, self).beginLoop(setup)
        self.counters.addCounter('cut_flow') 
        self.counters['cut_flow'].register('All events')
        self.counters['cut_flow'].register('>= 2 photons')
        #self.counters['cut_flow'].register('photon energy > 40')
        #self.counters['cut_flow'].register('pseudorapidity < 2.5')
        #self.counters['cut_flow'].register('2 b jets')
    
    def process(self, event):

        self.counters['cut_flow'].inc('All events')
        #if len(event.sel_iso_leptons) > 0:
        #    return True # could return False to stop processing
        #self.counters['cut_flow'].inc('No lepton')
        #jets = getattr(event, self.cfg_ana.input_jets)        
        #if len(jets) < 4:
        #    return True
        #self.counters['cut_flow'].inc('4 jets')
        #if min(jet.e() for jet in jets) >= 15.:
        #    self.counters['cut_flow'].inc('4 jets with E>15')
        #bjets = [jet for jet in jets if jet.tags['b']]
        #if len(bjets) >= 2:
        #    self.counters['cut_flow'].inc('2 b jets')
        
        #find 2 highest energy photons

        gammas = getattr(event, self.cfg_ana.photons)
	if len(gammas)<2:
	    return False
        self.counters['cut_flow'].inc('>= 2 photons')
        for gamma in gammas:
            if gamma.e() < 40:
                gammas.remove(gamma)
            elif abs(gamma.eta()) >= 2.5:
                gammas.remove(gamma)
        if len(gammas)<2:
            return False
        else:
            mass_square = (2*(gammas[0].e()*gammas[1].e()) - 2*numpy.dot(gammas[0].p3(),gammas[1].p3()))
        
        if len(gammas)>2:
            min_mass_diff = 9999.9
            photon_id_1 = -1
            photon_id_2 = -1
            for i in range(len(gammas)):
                for j in range(len(gammas)):
                    if i<j:
                        recoil_mass_square = ((240 - gammas[i].e() - gammas[j].e())**2 - numpy.dot((gammas[i].p3()+gammas[j].p3()),(gammas[i].p3()+gammas[j].p3())))
                        if recoil_mass_square < 0:
                            print 'Negative recoil mass squared'
                            break
                        else:
                            recoil_mass = math.sqrt(recoil_mass_square)
                        mass_diff = abs(recoil_mass - 91.2)
                        if mass_diff < min_mass_diff:
                            min_mass_diff = mass_diff
                            photon_id_1 = i
                            photon_id_2 = j
                            mass_square = (2*(gammas[i].e()*gammas[j].e()) - 2*numpy.dot(gammas[i].p3(),gammas[j].p3()))
        if mass_square < 0:
            mass = 0
            print 'Negative mass squared'
        else:
            mass = math.sqrt(mass_square) 
            print mass

        setattr(event, self.cfg_ana.hmass, mass)
