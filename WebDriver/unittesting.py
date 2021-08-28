"""
fichier de test qui vérifie certaines conditions dans le répertoire courant
"""

import unittest
import os

from WebDriver import tools_functions


class TestChromedriver(unittest.TestCase):

    def test_isfile(self):
        self.assertTrue(os.path.isfile('chromedriver.exe'))     # true
        self.assertFalse(os.path.isfile('chromedriver.zip'))     # false

    def test_get_version(self):
        self.assertEqual(tools_functions.get_version(), "92",
                         'format incorrect')

    def test_check_driver(self):
        self.assertEqual(tools_functions.check_driver(), "92",
                         'mauvais numéro de version')


if __name__ == '__main__':
    unittest.main()
