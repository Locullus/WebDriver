"""
script qui vérifie si le fichier chromedriver.exe existe dans le répertoire courant et sinon l'installe

"""

from classWebdriver import Webdriver

from tools_functions import check_isfile

# on s'assure que le chromedriver est bien installé et à jour
check_isfile('chromedriver.exe')

# on lance une session
url = "http://example.org/"
test = Webdriver(url)

# TODO : sur cette base on va pouvoir intégrer le module database pour ensuite lancer des sessions sur Boursorama
