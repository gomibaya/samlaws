import unittest
import logging
from SAsamlaws import main 
from SAsamlaws import SAsamlaws
from SAserialize import SAserialize
import os
from pathlib import Path


class Testsamlaws(unittest.TestCase):

    _CFGDIR = '.samlaws_test'
    _CFGFILE = 'config.yml'
    _REALCFGDIR = '.samlaws'

    def setUp(self):
        print('Preparando el contexto')
        home = str(Path.home())
        self.defconfig = { 'region': 'eu-west-1',
                          'outputformat': 'json',
                          'username': None,
                          'password': None,
                          'sslverification': True,
                          'idpentrydomain': None,
                          'idpentryurl': '/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices',
                          'role': None,
                          'awsconfigfile':
                            home +
                            os.path.sep +
                            '.aws' +
                            os.path.sep +
                            'credentials',                          
                          'sessionseconds': 3600}
        self.config1 = { 'region': 'eu-west-1',
                          'outputformat': 'json',
                          'username': 'test',
                          'password': 'test'}
        self.outputdir = str(os.getcwd()) + os.path.sep + 'output'
        self.testdir = str(os.getcwd()) + os.path.sep + 'tests'
        if not os.path.isdir(self.outputdir):
            os.mkdir(self.outputdir)
        self.dir = self.outputdir + os.path.sep + self._CFGDIR
        self.cfg = self.dir + os.path.sep + self._CFGFILE
        self.realhome = str(Path.home()) + os.path.sep + self._REALCFGDIR
        
    def test_config_default(self):
        print('default config')
        t = SAsamlaws(self.dir).showconfig()
        self.assertEqual(t, self.defconfig)

    def test_main_notvalidparams(self):
        print('main notvalidparams')
        try:
            os.mkdir(self.dir)
        except:
            pass
        writer = SAserialize(self.cfg)
        writer.serialize(self.config1)
        t = main(self.dir)
        # Si lo pongo después del assertion y falla, no borrará el contenido
        os.remove(self.cfg)
        os.rmdir(self.dir)          
        self.assertEqual(t, 1)

    #
    # Este test requiere que esté el fichero correcto en ~/.samlaws/config.yml
    # Lo copio de tests config.yml
    #
    def test_main_validparams(self):
        print('main validparams')
        reader = SAserialize(self.testdir + os.path.sep + self._CFGFILE).unserialize()
        if not os.path.isdir(self.realhome):
            os.mkdir(self.realhome)
        writer = SAserialize(self.realhome + os.path.sep + self._CFGFILE)
        writer.serialize(reader)
        t = main()   
        self.assertEqual(t, 0)       

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)
    unittest.main()
