"""
script qui vérifie si le fichier chromedriver.exe existe dans le répertoire courant et sinon l'installe
puis lance une session du driver afin de récupérer la liste des tournois où je suis engagé

"""

import os
from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import SessionNotCreatedException
import time

from classWebdriver import Webdriver
from tools_functions import check_isfile, close_pop_up, browser

# on charge les variables d'environnement
load_dotenv()
username = os.getenv("USER")
password = os.getenv("PASSWORD")

my_browser = browser()
try:
    my_browser.get("http://www.python.org")
    assert "Python" in my_browser.title
    elem = my_browser.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in my_browser.page_source
    time.sleep(10)
except SessionNotCreatedException:
    print("problème avec la version actuelle du chromedriver...")
my_browser.close()


# configuration du webdriver
options = Options()
options.headless = True     # configuration du driver en mode non visible
options.page_load_strategy = 'normal'

# on s'assure que le chromedriver est bien installé et à jour
check_isfile('chromedriver.exe')

# on définit l'url
url = "https://auth.fft.fr/auth/realms/master/protocol/openid-connect/auth?" \
      "client_id=FED_MET&response_type=code&scope=openid&redirect_uri=" \
      "https://tenup.fft.fr/user-auth/process"

# connection au site de la FFT
try:
    with Chrome(executable_path="chromedriver.exe", options=options) as driver:

        # on passe la fenêtre en plein écran
        # driver.maximize_window()

        # on lance la requête
        driver.get(url)

        # on attend que la page soit chargée
        driver.implicitly_wait(2)

        # on s'identifie pour accéder au compte
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_xpath("//*[@id='kc-form']/div[3]/button").click()

        driver.implicitly_wait(2)  # on peut aussi attendre un laps de temps déterminé avec : sleep(2)

        # on ferme la pop_up des cookies
        close_pop_up(driver)

        driver.find_element_by_class_name("menu-name").click()
        driver.implicitly_wait(2)

        driver.find_element_by_xpath(
            '//*[@id="page-header"]/div[2]/div/nav/ul/li[5]/div/div/ul/li[3]/ul/li[4]/a').click()
        result = driver.find_element_by_xpath('//*[@id="block-system-main"]/div/div/div/div[1]').text
        print(result)
        # time.sleep(10)
except SessionNotCreatedException:
    print("problème avec la version actuelle du chromedriver...")

# TODO : vérifier pourquoi la variable username renvoie bulam dans .env (j'ai dû en changer le nom pour être reconnu)
# TODO : une fenêtre de cookies s'ouvre et vient perturber le click sur le menu. Il faut gérer sa fermeture


# on peut aussi lancer une session en utilisant la classe Webdriver
driver = Webdriver("http://www.python.org")

# TODO : sur cette base on va pouvoir intégrer le module database pour ensuite lancer des sessions sur Boursorama
# TODO : on intégrera tout ceci dans une application flask avec une interface graphique correcte
