# -*- coding: utf-8 -*-

__author__ = "Esteban Barón"
__copyright__ = "Copyright 2020, Esteban Barón ,EBP"
__license__ = "MIT"
__email__ = "esteban@gominet.net"
__status__ = "Beta"
__version__ = "0.1.0b1"

from SAlogger import SAlogger
import os
# python 3.5
from pathlib import Path
import yaml


class SAconfig(SAlogger):
    _DEF_DIR = '.samlaws'
    _DEF_LISTFILE = 'conlist.yml'
    _TEMPLATES_TYPES = ('putty')
    _MSG = (
        'No puedo crear directorio {0}.',
        'Creado directorio {0}.',
        'No existe listado conexiones {0}.',
        'Template no soportado.',
        '{dir}{sep}templ{template}.txt',
        'No existe template {0}.'
        )

    _configpath = ''
    _listfile = ''

    """Configuracion aplicación"""
    def __init__(self, configpath=None):
        configpath = configpath or os.environ.get('DIRCONFIG', None)
        configpath = configpath or '{0}{1}{2}'.format(
            str(Path.home()),
            os.path.sep,
            self._DEF_DIR)
        # Para evitar problemas de mezcla absoluto relativo
        # internamente trabajo siempre con absoluto.
        configpath = os.path.abspath(configpath)

        SAlogger.__init__(self)

        if not os.path.isdir(configpath):
            try:
                os.mkdir(configpath)
            except OSError:
                self.critical(0, configpath)
            else:
                self.info(1, configpath)
        self._configpath = configpath
        self._listfile = self._filename_list()

    def _filename_list(self):
        ret = self._configpath + os.path.sep + self._DEF_LISTFILE
        if not os.path.isfile(ret):
            self.critical(2, ret)
            ret = ''
        return ret

    def filename_list(self):
        return self._listfile

    def _filename_template(self, template='putty'):
        ret = ''
        template = template.lower()
        if template not in self._TEMPLATES_TYPES:
            self.critical(3)
            return ret
        ret = self._MSG[4].format(
            dir=self._configpath,
            sep=os.path.sep,
            template=template)
        if not os.path.isfile(ret):
            self.critical(5, ret)
            ret = ''
        return ret

    def load_list(self):
        ret = {}
        if self._listfile:
            with open(self._listfile, 'r') as f:
                ret = yaml.safe_load(f)
        return ret

    def read_template(self, template='putty'):
        """Read template. De momento, sólo putty"""
        ftemplate = self._filename_template(template)
        ret = Path(ftemplate).read_text() if ftemplate else ''
        return ret


if __name__ == "__main__":
    print('Este fichero pertenece a un módulo, '
          'no es operativo como aplicación independiente.')
