import unittest
import tempfile
import copy
import os
import shutil

import heppy.framework.context as context

if context.name == 'fcc':
    
    from heppy.test.plot_ee_b import Plotter
    from heppy.framework.looper import Looper
    from heppy.configuration import PapasRuntype
    from ROOT import TFile
    PapasRuntype.from_fccsw = False
    from analysis_ee_Z_bb_cfg import config
    
    import logging
    logging.getLogger().setLevel(logging.ERROR)

    import heppy.statistics.rrandom as random
    from_fccsw = False

    class TestAnalysis_ee_Z_bb(unittest.TestCase):

        def setUp(self):
            random.seed(0xdeadbeef)
            self.outdir = tempfile.mkdtemp()
            import logging
            logging.disable(logging.CRITICAL)

        def tearDown(self):
            shutil.rmtree(self.outdir)
            logging.disable(logging.NOTSET)

        def test_beff_cms(self):
            '''Check b matching probability and b tag efficiency in CMS 
            '''
            from heppy.papas.detectors.CMS import cms
            fname = '/'.join([os.environ['HEPPY'],
                              'test/data/ee_Z_bbbar.root'])
            config.components[0].files = [fname]
            for s in config.sequence:
                if hasattr( s,'detector'):
                    s.detector = cms
            self.looper = Looper( self.outdir, config,
                                  nEvents=100,
                                  nPrint=0 )
            self.looper.loop()
            self.looper.write()
            rootfile = '/'.join([self.outdir,
                                'heppy.analyzers.JetTreeProducer.JetTreeProducer_1/jet_tree.root '])
            plotter = Plotter(rootfile)
            self.assertAlmostEqual(plotter.bfrac(), 0.83, places=2) #changing of random seed varies this between approx 0.78 and 0.83
            self.assertAlmostEqual(plotter.beff(), 0.70, places=2) #changing of seed  varies this from 0.63/0.68 etc
    
        def test_fake_cms(self):
            '''Check fake rate in CMS
            '''
            from heppy.papas.detectors.CMS import cms
            #fname = '/'.join([os.environ['HEPPY'],
            #                  'test/data/ee_Z_ddbar.root'])
            fname = '/'.join([os.environ['HEPPY'],
                                      'test/data/ee_Z_ddbar_with_papas_rec.root'])    
            config.components[0].files = [fname]
            for s in config.sequence:
                if hasattr( s,'detector'):
                    s.detector = cms
            self.looper = Looper( self.outdir, config,
                                  nEvents=100,
                                  nPrint=0 )
            self.looper.loop()
            self.looper.write()
            rootfile = '/'.join([self.outdir,
                                 'heppy.analyzers.JetTreeProducer.JetTreeProducer_1/jet_tree.root '])

##            mean, sigma = plot(rootfile)
##            self.assertAlmostEqual(mean, 94.6, 1)
##            self.assertAlmostEqual(sigma, 15.1, 1)

##        def test_z_clic(self):
##            '''Check for an almost perfect match with reference.
##            Will fail if physics algorithms are modified,
##            so should probably be removed from test suite,
##            or better: be made optional. 
##            '''
##            from heppy.papas.detectors.CLIC import clic
##            fname = '/'.join([os.environ['HEPPY'],
##                                      'test/data/ee_Z_ddbar.root'])
##            config.components[0].files = [fname]
##            config.sequence[2].detector = clic
##            self.looper = Looper( self.outdir, config,
##                                  nEvents=100,
##                                  nPrint=0 )            
##            self.looper.loop()
##            self.looper.write()
##            rootfile = '/'.join([self.outdir,
##                                'heppy.analyzers.GlobalEventTreeProducer.GlobalEventTreeProducer_1/tree.root'])
##            mean, sigma = plot(rootfile)
##            self.assertAlmostEqual(mean, 83.24, 1)
##            self.assertAlmostEqual(sigma, 7.37, 1)
##
  

        

if __name__ == '__main__':

    unittest.main()
