from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter
from heppy.particles.tlv.resonance import Resonance2 as Resonance

import math
import numpy
class Selection(Analyzer):

    def beginLoop(self, setup):
        super(Selection, self).beginLoop(setup)
        self.counters.addCounter('cut_flow') 
        self.counters['cut_flow'].register('All events')
        self.counters['cut_flow'].register('>= 2 photons')
        self.counters['cut_flow'].register('e>=40GeV')
        self.counters['cut_flow'].register('eta < 2.5')
        self.counters['cut_flow'].register('sum of photon isolations < 0.4')
        self.counters['cut_flow'].register('pseudorapidity gap < 1.8')
        self.counters['cut_flow'].register('Higgs candidate beam angle > 25 degrees')
    
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
        

        gammas2 = getattr(event, self.cfg_ana.photons) 
	if len(gammas2)<2:
	    return False
        self.counters['cut_flow'].inc('>= 2 photons')
        gammas1 = [gamma1 for gamma1 in gammas2 if (gamma1.e()>=40)]
        if len(gammas1)<2:
            return False
        self.counters['cut_flow'].inc('e>=40GeV')
        gammas = [gamma for gamma in gammas1 if abs(gamma.eta())<2.5]
        if len(gammas)<2:
            return False
        self.counters['cut_flow'].inc('eta < 2.5')
       
        if len(gammas)==2:
            higgscandidates = (gammas[0], gammas[1]) 
        
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
            higgscandidates = (gammas[photon_id_1],gammas[photon_id_2])
        
        isosum = 0
        for candidate in higgscandidates:
            isolation = candidate.iso.sume/candidate.e()
            isosum += isolation
        if isosum >= 0.4:
            return False
        self.counters['cut_flow'].inc('sum of photon isolations < 0.4')

        etagap = abs(higgscandidates[0].eta() - higgscandidates[1].eta())
        if etagap >= 1.8:
            return False
        self.counters['cut_flow'].inc('pseudorapidity gap < 1.8')

        higgs = Resonance(higgscandidates[0], higgscandidates[1], 25)
        if numpy.degrees(abs(higgs.theta())) >= 65:
            return False
        self.counters['cut_flow'].inc('Higgs candidate beam angle > 25 degrees')

        mass_square = (2*(higgscandidates[0].e()*higgscandidates[1].e()) - 2*numpy.dot(higgscandidates[0].p3(),higgscandidates[1].p3()))

        if mass_square < 0:
            mass = 0
            print 'Negative mass squared'
        else:
            mass = math.sqrt(mass_square) 

        setattr(event, self.cfg_ana.higgs, higgs)
        setattr(event, self.cfg_ana.photons, higgscandidates)

                                     
        
#        if mass<100:
#            print mass
#            print higgscandidates[0].e()
#            print higgscandidates[1].e()
#            print higgscandidates[0].eta()
#            print higgscandidates[1].eta()
#            recoil_mass = math.sqrt((240 - higgscandidates[0].e() - higgscandidates[1].e())**2 - numpy.dot((higgscandidates[0].p3()+higgscandidates[1].p3()),(higgscandidates[0].p3()+higgscandidates[1].p3())))
#            print recoil_mass
#            isosum = higgscandidates[0].iso.sume/higgscandidates[0].e() + higgscandidates[0].iso.sume/higgscandidates[1].e()
#            print isosum
#            print etagap

            
