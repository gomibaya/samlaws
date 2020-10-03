# -*- coding: utf-8 -*-

__author__ = "Esteban Barón"
__copyright__ = "Copyright 2020, Esteban Barón ,EBP"
__license__ = "MIT"
__email__ = "esteban@gominet.net"
__status__ = "Beta"
__version__ = "0.1.0b1"

from SAlogger import SAlogger
from SAserialize import SAserialize
import os
# python 3.5
from pathlib import Path


class SAconfig(SAlogger):
    _DEF_DIR = '.samlaws'
    _DEF_CFGFILE = 'config.yml'
    _MSG = (
        'No puedo crear directorio {0}.',
        'Creado directorio {0}.',
        'No existe fichero configuración {0}.'
        )

    _configpath = ''
    _cfgfile = ''

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
        self._cfgfile = self._filename_cfg()

    def _filename_cfg(self):
        ret = self._configpath + os.path.sep + self._DEF_CFGFILE
        if not os.path.isfile(ret):
            self.critical(2, ret)
            ret = ''
        return ret

    def filename_cfg(self):
        return self._cfgfile

    def load_cfg(self, defaults=None):
        ret = SAserialize().unserialize(self._cfgfile)
        if defaults:
            for item in defaults:
                tmp = ret.get(item, defaults[item])
                ret[item] = tmp
        return ret


if __name__ == "__main__":
    print('Este fichero pertenece a un módulo, '
          'no es operativo como aplicación independiente.')
