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
        self.counters['cut_flow'].register('No mumu pair')
        self.counters['cut_flow'].register('Relative isolation > 0.2')
        self.counters['cut_flow'].register('80 < recoil mass < 110')
        #self.counters['cut_flow'].register('sum of photon isolations < 0.4')
        #self.counters['cut_flow'].register('pseudorapidity gap < 1.8')
        #self.counters['cut_flow'].register('Higgs candidate beam angle > 25 degrees')
    
    def process(self, event):

        self.counters['cut_flow'].inc('All events')

        mus = getattr(event, self.cfg_ana.muons)
        photons = getattr(event, self.cfg_ana.photons)

        posmus = [mu for mu in mus if mu.pdgid() == -13]
        negmus = [mu for mu in mus if mu.pdgid() == 13]
        if len(posmus)<1 or len(negmus)<1:
            return False
        self.counters['cut_flow'].inc('No mumu pair') #why would there be no mumu pair?


        




        
        self.counters['cut_flow'].inc('Relative isolation > 0.2') #check this section!




  #change this bit!
        part1 = 240 - mu1.e() - mu2.e()
        part2 = mu1.p3() + mu2.p3()
        for i in range(len(photons)):
            part1 -= photons[i].e()
            part2 += photons[i].p3()
        recoil_mass_square = part1**2 - numpy.dot(part2, part2)
        if recoil_mass_square<0:
            print 'Negative recoil mass squared'
            recoil_mass = 0
        else:
            recoil_mass = math.sqrt(recoil_mass_square)
        if recoil_mass <= 80 or recoil_mass >= 110:
            return False
        self.counters['cut_flow'].inc('80 < recoil mass < 110')
        

        #setattr(event, self.cfg_ana.higgs, higgs)
        #setattr(event, self.cfg_ana.photons, higgscandidates)

        


        #gammas = [gamma for gamma in gammas if (gamma.e()>=40 and abs(gamma.eta())<2.5)]
        #if len(gammas)<2:
        #    return False
        #self.counters['cut_flow'].inc('e>=40GeV, eta < 2.5')
        #gammas[:] = [gamma for gamma in gammas if abs(gamma.eta())<2.5]
        #if len(gammas)<2:
        #    return False
        #if len(gammas)==2:
        #    higgscandidates = (gammas[0], gammas[1]) 
        #
        #if len(gammas)>2:
        #    min_mass_diff = 9999.9
        #    photon_id_1 = -1
        #    photon_id_2 = -1
        #    for i in range(len(gammas)):
        #        for j in range(len(gammas)):
        #            if i<j:
        #                recoil_mass_square = ((240 - gammas[i].e() - gammas[j].e())**2 - numpy.dot((gammas[i].p3()+gammas[j].p3()),(gammas[i].p3()+gammas[j].p3())))
        #                if recoil_mass_square < 0:
        #                    print 'Negative recoil mass squared'
        #                    break
        #                else:
        #                    recoil_mass = math.sqrt(recoil_mass_square)
        #                mass_diff = abs(recoil_mass - 91.2)
        #                if mass_diff < min_mass_diff:
        #                    min_mass_diff = mass_diff
        #                    photon_id_1 = i
        #                    photon_id_2 = j
        #    higgscandidates = (gammas[photon_id_1],gammas[photon_id_2])        
        #isosum = 0
        #for candidate in higgscandidates:
        #    isolation = candidate.iso.sume/candidate.e()
        #    isosum += isolation
        #if isosum >= 0.4:
        #    return False
        #self.counters['cut_flow'].inc('sum of photon isolations < 0.4')
        #etagap = abs(higgscandidates[0].eta() - higgscandidates[1].eta())
        #if etagap >= 1.8:
        #    return False
        #self.counters['cut_flow'].inc('pseudorapidity gap < 1.8')
        #higgs = Resonance(higgscandidates[0], higgscandidates[1], 25)
        #if numpy.degrees(abs(higgs.theta())) >= 65:
        #    return False
        #self.counters['cut_flow'].inc('Higgs candidate beam angle > 25 degrees')
        #mass_square = (2*(higgscandidates[0].e()*higgscandidates[1].e()) - 2*numpy.dot(higgscandidates[0].p3(),higgscandidates[1].p3()))
        #if mass_square < 0:
        #    mass = 0
        #    print 'Negative mass squared'
        #else:
        #    mass = math.sqrt(mass_square) 

        #setattr(event, self.cfg_ana.higgs, higgs)
        #setattr(event, self.cfg_ana.photons, higgscandidates)

                                     
        
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

            
