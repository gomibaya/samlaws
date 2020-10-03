import unittest
import logging
from SAconfig import SAconfig
import os
from pathlib import Path
import json


class TestSAconfig(unittest.TestCase):

    def setUp(self):
        print('Test SAconfig')
        self.dir = str(Path.home()) + os.path.sep + '.samlaws'
        self.list = self.dir + os.path.sep + 'conlist.yml'
        self.listdata1 = [{'name': 'prueba'}]
        self.templateputty = self.dir + os.path.sep + 'templ' + 'putty'

    def test_createdir_ok(self):
        print('Sin directorio. Crea en el home')
        SAconfig()
        cpath = str(Path.home()) + os.path.sep + '.samlaws'
        t = os.path.isdir(cpath)
        self.assertEqual(t, True)
        
    def test_createdir_param(self):
        print('Con directorio. Crea en directorio trabajo')
        SAconfig('dirprueba')
        cpath = str(os.getcwd()) + os.path.sep + 'dirprueba'
        t = os.path.isdir(cpath)
        self.assertEqual(t, True)
        os.rmdir(cpath)

    def test_filenameList_unexistent(self):
        print('Obtener el filenameList, no existe')
        try:
            os.remove(self.list)
        except Exception:
            pass
        config = SAconfig()
        t = config.filename_list()
        self.assertEqual(t, '')

    def test_filenameList_existent(self):
        print('Obtener el filenameList, existe')
        # he de crearlo antes de iniciarlizar el config
        # que lo lee sólo al principio
        cpath = str(os.getcwd()) + os.path.sep + 'dirprueba'
        list = cpath + os.path.sep + 'conlist.yml'
        os.mkdir(cpath)     
        with open(list,'w+') as f:
            f.write(json.dumps(self.listdata1))
        config = SAconfig('dirprueba')
        t = config.filename_list()
        # Si lo pongo después del assertion y falla, no borrará el contenido
        os.remove(list)
        os.rmdir(cpath)        
        self.assertEqual(t, list)

    def test_loadList_existent(self):
        print('Obtener el objeto de filenameList, existe')
        # he de crearlo antes de iniciarlizar el config
        # que lo lee sólo al principio
        cpath = str(os.getcwd()) + os.path.sep + 'dirprueba'
        list = cpath + os.path.sep + 'conlist.yml'
        os.mkdir(cpath)     
        with open(list,'w+') as f:
            f.write(json.dumps(self.listdata1))
        config = SAconfig('dirprueba')
        t = config.load_list()
        # Si lo pongo después del assertion y falla, no borrará el contenido
        os.remove(list)
        os.rmdir(cpath)        
        self.assertEqual(t, self.listdata1)

    def test_filenameTemplate_putty_vacio(self):
        print('Obtener el filenameTemplate')
        config = SAconfig()
        t = config.read_template('putty')
        self.assertEqual(t, '')

    def test_filenameTemplate_putty_caseupper_vacio(self):
        print('Obtener el filenameTemplate')
        config = SAconfig()
        t = config.read_template('Putty')
        self.assertEqual(t, '')

    def test_filenameTemplate_nosupported_fail(self):
        print('Obtener el filenameTemplate')
        config = SAconfig()
        t = config.read_template('Other')
        self.assertEqual(t, '')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)
    unittest.main()
