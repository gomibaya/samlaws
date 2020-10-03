# -*- coding: utf-8 -*-

__author__ = "Esteban Barón"
__copyright__ = "Copyright 2020, Esteban Barón ,EBP"
__license__ = "MIT"
__email__ = "esteban@gominet.net"
__status__ = "Beta"
__version__ = "0.1.0b1"

from SAlogger import SAlogger
import yaml
from yaml.parser import ParserError
from yaml.scanner import ScannerError
import json
# python 3.5
from pathlib import Path


class SAformatError(Exception):
    pass


class SAserialize(SAlogger):

    _MSG = (
        'Formato no soportado de fichero: {0}.',
        'Error al unserializar fichero {0} : {1}.',
        'Error al serializar fichero {0} : {1}.'
        )

    _UNSERIALIZEFORMAT = {}
    _SERIALIZEFORMAT = {}

    _filename = None

    """Configuracion aplicación"""
    def __init__(self, filename=None):
        self._UNSERIALIZEFORMAT = {
            '.yml': self._unserialize_yaml,
            '.json': self._unserialize_json
        }
        self._SERIALIZEFORMAT = {
            '.yml': self._serialize_yaml,
            '.json': self._serialize_json
        }
        SAlogger.__init__(self)
        self._filename = filename

    def _unserialize_yaml(self, filename):
        ret = {}
        with open(filename, 'r') as f:
            try:
                ret = yaml.safe_load(f)
            except (ScannerError, ParserError) as e:
                raise SAformatError(str(e))
        return ret

    def _unserialize_json(self, filename):
        ret = {}
        with open(filename, 'r') as f:
            ret = json.load(f)
        return ret

    def unserialize(self, filename=None):
        ret = {}
        wfilename = filename if filename else self._filename
        if not wfilename:
            return ret
        suffix = Path(wfilename).suffix.lower()
        if suffix in self._UNSERIALIZEFORMAT:
            f = self._UNSERIALIZEFORMAT[suffix]
        else:
            msg = self.critical(0, wfilename)
            raise ValueError(msg)
        try:
            ret = f(wfilename)
        except (OSError, IOError, SAformatError) as e:
            self.critical(1, wfilename, str(e))
        return ret

    def _serialize_yaml(self, data, filename):
        ret = True
        with open(filename, 'w+') as f:
            try:
                yaml.dump(data, f)
            except (ScannerError, ParserError) as e:
                raise SAformatError(str(e))
        return ret

    def _serialize_json(self, data, filename):
        ret = True
        with open(filename, 'w+') as f:
            self._logger.debug('Escribir a {0} data {1}'.
                               format(filename, data))
            json.dump(data, f)
        return ret

    def serialize(self, data, filename=None):
        ret = False
        wfilename = filename if filename else self._filename
        if not wfilename:
            return ret
        suffix = Path(wfilename).suffix.lower()
        if suffix in self._SERIALIZEFORMAT:
            f = self._SERIALIZEFORMAT[suffix]
        else:
            msg = self.critical(0, wfilename)
            raise ValueError(msg)
        try:
            ret = f(data, wfilename)
        except (OSError, IOError, SAformatError) as e:
            self.critical(2, wfilename, str(e))
        return ret


if __name__ == "__main__":
    print('Este fichero pertenece a un módulo, '
          'no es operativo como aplicación independiente.')
