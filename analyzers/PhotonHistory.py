'''Select stable generated charged hadrons from b-quark decay'''


from heppy.framework.analyzer import Analyzer
from heppy.particles.genbrowser import GenBrowser
from heppy.particles.pdgcodes import hasBottom

class PhotonHistory(Analyzer):
    '''Select stable generated charged hadrons from b-quark decay'''

    def process(self, event):
        '''event should contain:
        
        * gen_particles: list of all stable gen particles
        '''
        genptcs = event.gen_particles
        genphotons=[]
        for ptc in genptcs:
            if abs(ptc.pdgid())==22:
                genphotons.append(ptc)
        if len(genphotons) == 0:
            return
        event.genbrowser = GenBrowser(event.gen_particles,
                                      event.gen_vertices)
           
        
