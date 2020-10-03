# -*- coding: utf-8 -*-

__author__ = "Esteban Barón"
__copyright__ = "Copyright 2020, Esteban Barón ,EBP"
__license__ = "MIT"
__email__ = "esteban@gominet.net"
__status__ = "Beta"
__version__ = "0.1.0b1"

import logging


class SAlogger(object):

    _DEFAULTMSG = 'Error en log. No existe el codigo proporcionado'

    """Configuracion aplicación"""
    def __init__(self, logger=None):
        self._logger = logger or logging.getLogger(self.__class__.__name__)

    def __log(self, level, idxmsg, *args):
        try:
            msg = self._MSG[idxmsg]
        except AttributeError:
            msg = self._DEFAULTMSG
        fmsg = msg.format(*args)
        self._logger.log(level, fmsg)
        return fmsg

    def debug(self, idxmsg, *args):
        return self.__log(logging.DEBUG, idxmsg, *args)

    def info(self, idxmsg, *args):
        return self.__log(logging.INFO, idxmsg, *args)

    def warning(self, idxmsg, *args):
        return self.__log(logging.WARNING, idxmsg, *args)

    def critical(self, idxmsg, *args):
        return self.__log(logging.CRITICAL, idxmsg, *args)

    def error(self, idxmsg, *args):
        return self.__log(logging.ERROR, idxmsg, *args)


if __name__ == "__main__":
    print('Este fichero pertenece a un módulo, '
          'no es operativo como aplicación independiente.')
