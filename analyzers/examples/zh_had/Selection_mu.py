from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter
from itertools import combinations
from heppy.particles.tlv.resonance import Resonance2 as Resonance

import math
import numpy
class Selection(Analyzer):

    def beginLoop(self, setup):
        super(Selection, self).beginLoop(setup)
        self.counters.addCounter('cut_flow') 
        self.counters['cut_flow'].register('All events')
        self.counters['cut_flow'].register('Mumu pair')
        self.counters['cut_flow'].register('Relative isolation < 0.2')
        self.counters['cut_flow'].register('80 < recoil mass < 110')
        self.counters['cut_flow'].register('Two visible jets')
        self.counters['cut_flow'].register('EM fraction < 0.8')
    
    def process(self, event):

        self.counters['cut_flow'].inc('All events')

        mus = getattr(event, self.cfg_ana.muons)
        photons = getattr(event, self.cfg_ana.photons)

        posmus = [mu for mu in mus if mu.pdgid() == -13]
        negmus = [mu for mu in mus if mu.pdgid() == 13]
        if len(posmus)<1 or len(negmus)<1:
            return False
        self.counters['cut_flow'].inc('Mumu pair') #why would there be no mumu pair?

        isomus = [mu for mu in mus if mu.iso.sumpt/mu.pt()<0.2] #check relative isolation
        posmus = [mu for mu in isomus if mu.pdgid() == -13]
        negmus = [mu for mu in isomus if mu.pdgid() == 13] 
        if len(posmus)<1 or len(negmus)<1:
            return False
        self.counters['cut_flow'].inc('Relative isolation < 0.2')
	
        #idea: try all combinations of measured photons to see which system of some photons + muons produces recoil mass closest to the Z mass
        photon_combos = sum([map(list, combinations(photons, k)) for k in range(len(photons) + 1)], [])
#        print len(photon_combos)
#      	print len(photons)
        #this uses itertools.combinations to create a list of all the possible combinations of photons
#        min_mass_diff = 9999.9
#        recoilmass = 0
        pos_mus = [] 
        neg_mus = []
#        for i in range(len(posmus)):
#            mu1 = posmus[i]
#            for j in range(len(negmus)):
#                mu2 = negmus[j]
#                part1 = 240 - mu1.e() - mu2.e()
#                part2 = mu1.p3() + mu2.p3()
#                for l in range(len(photon_combos)):
#                    for m in range(len(photon_combos[l])):
#                        part1 -= photon_combos[l][m].e()
#                        part2 += photon_combos[l][m].p3()
#                    recoil_mass_square = part1**2 - numpy.dot(part2, part2)
#                    if recoil_mass_square<0:
#                        print 'Negative recoil mass squared'
#                        recoil_mass = 0
#                    else:
#                        recoil_mass = math.sqrt(recoil_mass_square)
#                    mass_diff = abs(recoil_mass - 91.2)                                                         
#                    if mass_diff < min_mass_diff:                                                               
#                        min_mass_diff = mass_diff
#                        recoilmass = recoil_mass

#        part1 = 240
#        part2 = numpy.zeros(3)
#        for l in range(len(photon_combos)):
#            for m in range(len(photon_combos[l])):
#                part1 -= photon_combos[l][m].e()
#                part2 += photon_combos[l][m].p3()
#            for i in range(len(posmus)):
#                mu1 = posmus[i]
#                part1 -= mu1.e()
#                part2 += mu1.p3()
#                for j in range(len(negmus)):
#                    mu2 = negmus[j]
#                    part1 -= mu2.e()
#                    part2 += mu2.p3()
#                    recoil_mass_square = part1**2 - numpy.dot(part2, part2)                                      
#                    if recoil_mass_square<0:                                                                    
#                        print 'Negative recoil mass squared'                
#                        recoil_mass = 0                       
#                    else:                                                                                      
#                        recoil_mass = math.sqrt(recoil_mass_square)                                             
#                    mass_diff = abs(recoil_mass - 91.2)                                                         
#                    if mass_diff < min_mass_diff:                                                               
#                        min_mass_diff = mass_diff                                        
#                        recoilmass = recoil_mass
#                if recoilmass <= 80 or recoilmass >= 110:
#                    return False
#                else:
#                    pos_mus.append(mu1)
#                    neg_mus.append(mu2)
#                    print recoilmass
                    
        #pos_mus and neg_mus may contain repeats of the muons or antimuons but, ordered, they contain a list of pairs that survive the cuts

#        if len(pos_mus)!= len(neg_mus):
#            print 'this is bad!'
#
#        if len(pos_mus) < 1:
#            return False
#        self.counters['cut_flow'].inc('80 < recoil mass < 110')
        

        #continuing assuming the above has worked!
        
        





        #setattr(event, self.cfg_ana.higgs, higgs)
        #setattr(event, self.cfg_ana.photons, higgscandidates)

        


