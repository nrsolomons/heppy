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
        photons = event.genphotons
        event.genbrowser = GenBrowser(event.genphotons,
                                      event.gen_vertices) 
           
        
