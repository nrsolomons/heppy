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
        self.counters['cut_flow'].inc('Mumu pair') 

        isomus = [mu for mu in mus if mu.iso.sumpt/mu.pt()<0.2]
        posmus = [mu for mu in isomus if mu.pdgid() == -13]
        negmus = [mu for mu in isomus if mu.pdgid() == 13] 
        if len(posmus)<1 or len(negmus)<1:
            return False
        self.counters['cut_flow'].inc('Relative isolation < 0.2')
	
	bremphotons = []
	for i in photons:
	    for j in isomus:
		if deltaR(i,j)<0.5:
		    bremphotons.append(i)

       # pos_mus and neg_mus may contain repeats of the muons or antimuons but, ordered, they contain a list of pairs that survive the cuts
        photon_combos = sum([map(list, combinations(bremphotons, k)) for k in range(len(bremphotons) + 1)], []) 
        min_mass_diff = 9999.9
        recoilmass = 0
        pos_mus = [] 
        neg_mus = []

        for i in range(len(posmus)):
            mu1 = posmus[i]
            for j in range(len(negmus)):
                mu2 = negmus[j]
                part1 = 240 - mu1.e() - mu2.e()
                part2 = mu1.p3() + mu2.p3()
                for l in range(len(photon_combos)):
                    for m in range(len(photon_combos[l])):
                        part1 -= photon_combos[l][m].e()
                        part2 += photon_combos[l][m].p3()
                    recoil_mass_square = part1**2 - numpy.dot(part2, part2)
                    if recoil_mass_square<0: 
                        recoil_mass = 0
                    else:
                        recoil_mass = math.sqrt(recoil_mass_square)
                    mass_diff = abs(recoil_mass - 91.2)                    
                    if mass_diff < min_mass_diff:                     
                        min_mass_diff = mass_diff
                        recoilmass = recoil_mass

                if recoilmass <= 80 or recoilmass >= 110:
                    return False
                else:
                    pos_mus.append(mu1)
                    neg_mus.append(mu2)

        if len(pos_mus) < 1:
            return False
        self.counters['cut_flow'].inc('80 < recoil mass < 110')

	jets1 = getattr(event, self.cfg_ana.input_jets)
        jets = []
        for jet in jets1:
            if jet.e()>0:
                jets.append(jet)
            else:
                return False
	if len(jets)<2:
	    return False
	self.counters['cut_flow'].inc('Two visible jets')
	
	notphoton = []
	for jet in jets:
            emfrac = (jet.constituents[211].e() + jet.constituents[22].e())/jet.e()
	    if emfrac < 0.8:
		notphoton.append(jet)
	if len(notphoton)<1:
	    return False 
        self.counters['cut_flow'].inc('EM fraction < 0.8')

        if len(pos_mus) > 1:
            min_mass_diff = 9999.9
            id1 = -1
            id2 = -1
            for i in range(len(pos_mus)):
                for j in range(len(neg_mus)):
                    mass_square = 2*(pos_mus[i].e()*neg_mus[j].e()) - 2*numpy.dot(pos_mus[i].p3(),neg_mus[j].p3())
                    if mass_square < 0:
                        print 'Negative mass squared'
                        break
                    else:
                        mass = math.sqrt(mass_square)
                    mass_diff = abs(mass - 125.1)
                    if mass_diff < min_mass_diff:
                        id1 = i
                        id2 = j
            higgscandidates = (pos_mus[id1], neg_mus[id2])
        else:
            higgscandidates = (pos_mus[0], neg_mus[0])

	higgs = Resonance(higgscandidates[0], higgscandidates[1], 25)
	setattr(event, self.cfg_ana.higgs, higgs)
        setattr(event, self.cfg_ana.muons, higgscandidates)
