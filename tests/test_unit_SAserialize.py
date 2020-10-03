import unittest
import logging
from SAserialize import SAserialize
import os
from pathlib import Path


class TestSAserialize(unittest.TestCase):
    
    _CFGDIR = '.samlaws_test'
    _CFGFILE = 'config.yml'

    def setUp(self):
        print('Test SAserialize')
        self.dir = str(Path.home()) + os.path.sep + self._CFGDIR
        self.list = self.dir + os.path.sep + self._CFGFILE
        self.sourcelist1 = 'valor: prueba'
        self.objectlist1 = {'valor': 'prueba'}
        self.serializer = SAserialize(self.list)
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)

    def test_unserialize_nosupported(self):
        print('Carga file no soportado')
        with self.assertRaises(ValueError) as context:
            self.serializer.unserialize('file.txt')         
        self.assertTrue('Formato no soportado de fichero' in str(context.exception))
        
    def test_unserialize_unexistent(self):
        print('Carga file no existente')
        data = self.serializer.unserialize('file456789.yml')
        self.assertEqual(data, {})

    def test_serialize_ok(self):
        print('Serialize a fichero')
        self.serializer.serialize(self.objectlist1)
        self.assertTrue(os.path.isfile(self.list))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)
    unittest.main()
