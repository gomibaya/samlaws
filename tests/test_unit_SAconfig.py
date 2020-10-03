import unittest
import logging
from SAconfig import SAconfig
from SAserialize import SAserialize
import os
from pathlib import Path
import shutil


class TestSAconfig(unittest.TestCase):
    
    _CFGDIR = '.samlaws_test'
    _CFGFILE = 'config.yml'
    _REALCFGDIR = '.samlaws'

    def setUp(self):
        print('Test SAconfig')
        self.outputdir = str(os.getcwd()) + os.path.sep + 'output'
        if not os.path.isdir(self.outputdir):
            os.mkdir(self.outputdir)        
        self.dir = self.outputdir + os.path.sep + self._CFGDIR
        self.cfg = self.dir + os.path.sep + self._CFGFILE
        self.listdata1 = [{'name': 'prueba'}]

    def test_createdir_ok(self):
        print('Sin directorio. Crea en el home')
        cpath = str(Path.home()) + os.path.sep + self._REALCFGDIR
        shutil.rmtree(cpath, ignore_errors=True)
        SAconfig()
        t = os.path.isdir(cpath)
        os.rmdir(cpath)
        self.assertEqual(t, True)
        
    def test_createdir_param(self):
        print('Con directorio. Crea en directorio trabajo')
        SAconfig(self.dir)
        t = os.path.isdir(self.dir)
        os.rmdir(self.dir)
        self.assertEqual(t, True)

    def test_filenamecfg_unexistent(self):
        print('Obtener el filenamecfg, no existe')
        try:
            os.remove(self.cfg)
        except Exception:
            pass
        config = SAconfig(self.dir)
        t = config.filename_cfg()
        self.assertEqual(t, '')

    def test_filenamecfg_existent(self):
        print('Obtener el filenamecfg, existe')
        # he de crearlo antes de iniciarlizar el config
        # que lo lee sólo al principio
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)         
        writer = SAserialize(self.cfg)
        writer.serialize(self.listdata1)
        self.assertTrue(os.path.isfile(self.cfg))

        config = SAconfig(self.dir)
        t = config.filename_cfg()
        # Si lo pongo después del assertion y falla, no borrará el contenido
        os.remove(self.cfg)
        os.rmdir(self.dir)        
        self.assertEqual(t, self.cfg)

    def test_loadcfg_existent(self):
        print('Obtener el objeto de filenamecfg, existe')
        # he de crearlo antes de iniciarlizar el config
        # que lo lee sólo al principio
        writer = SAserialize(self.cfg)
        writer.serialize(self.listdata1)             

        config = SAconfig(self.dir)
        t = config.load_cfg()
        # Si lo pongo después del assertion y falla, no borrará el contenido
        os.remove(self.cfg)
        os.rmdir(self.dir)        
        self.assertEqual(t, self.listdata1)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)
    unittest.main()
