"""
script qui vérifie si le fichier chromedriver.exe existe dans le répertoire courant et sinon l'installe

"""

from classWebdriver import Webdriver

from tools_functions import check_isfile

# on s'assure que le chromedriver est bien installé et à jour
check_isfile('chromedriver.exe')

# on lance une session
driver = Webdriver("http://www.python.org")

# TODO : sur cette base on va pouvoir intégrer le module database pour ensuite lancer des sessions sur Boursorama
# TODO : on intégrera tout ceci dans une application flask avec une interface graphique correcte
