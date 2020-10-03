# -*- coding: utf-8 -*-

__author__ = "Esteban Barón"
__copyright__ = "Copyright 2020, Esteban Barón ,EBP"
__license__ = "MIT"
__email__ = "esteban@gominet.net"
__status__ = "Beta"
__version__ = "0.1.0b1"

from SAlogger import SAlogger
from CBload import CBload
from SAconfig import SAconfig
from CBwriter import CBwriter


class SAsamlaws(SAlogger):

    _MSG = (
        'Inicio samlaws',
        'Name: {0} , Type: {1}'
        )

    def __init__(self):
        SAlogger.__init__(self)
        self.debug(0)

    def main(self):
        ret = 0
        config = SAconfig()
        load = CBload(config)
        # logger.debug('El list es {0}'.format(load.list()))
        conlist = load.list()
        if conlist:
            for item in conlist:
                name = item.get('Name',None)
                type = item.get('Type',None)
                self.debug(1, name, type)
            writer = CBwriter(config)
            writer.processitems(conlist)
        return ret


def main():
    objexec = SAsamlaws()
    return objexec.main()
# end def main


if __name__ == "__main__":
    print("Este fichero pertenece a un módulo, "
          "no es operativo como aplicación independiente.")
