import unittest
import logging
from SAsamlaws import main 


class Testsamlaws(unittest.TestCase):

    def setUp(self):
        print('Preparando el contexto')

    def test_main_ok(self):
        print('main correcto')
        t = main()
        self.assertEqual(t, 0)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)
    unittest.main()
