"""
fichier de test qui vérifie certaines conditions dans le répertoire courant
"""

import unittest
import os

import tools_functions


class TestChromedriver(unittest.TestCase):

    # on vérifie la présence de fichiers
    def test_isfile(self):
        self.assertTrue(os.path.isfile('chromedriver.exe'))         # true
        self.assertFalse(os.path.isfile('chromedriver.zip'))        # false
        self.assertTrue(os.path.isfile('chromedriver_version'))     # True

    # on vérifie que la fonction retourne bien un nombre à deux chiffres
    def test_get_version(self):
        self.assertRegex(tools_functions.get_version(), "\\d{2}")

    # on vérifie que la fonction retourne bien un nombre à deux chiffres
    def test_check_driver(self):
        self.assertRegex(tools_functions.get_version(), "\\d{2}")

    # on vérifie que le numéro de version enregistré dans le fichier chromedriver_version est à 2 chiffres
    def test_chromedriver_version_file(self):
        self.assertRegex(tools_functions.get_datas('chromedriver_version'), "\\d{2}")


if __name__ == '__main__':
    unittest.main()
