import unittest
import logging
from SAlogger import SAlogger

class testlog(SAlogger):
    _MSG = (
        'Msg sin params.',
        'Msg with 1 param {0}.'
        )

    def __init__(self):
        SAlogger.__init__(self)


class TestSAlogger(unittest.TestCase):

    def setUp(self):
        print('Test SAlogger')

    def test_init_withoutlogger(self):
        print('init sin logger')
        log = SAlogger()
        log.info(1)

    def test_init_withoutlogger_withparams(self):
        print('init sin logger con parametros')
        log = SAlogger()
        log.info(1, 'hola')

    def test_init_incorrectindex(self):
        print('init con index incorrecto')
        log = testlog()
        log.info(1, 'hola')

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)
    unittest.main()
