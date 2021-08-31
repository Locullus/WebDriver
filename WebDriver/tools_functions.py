import os
import re
import pickle
import requests
from requests_html import HTMLSession
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from zipfile import ZipFile


def save_datas(my_file, data):
    """ fonction qui enregistre les données dans un fichier externe """
    with open(my_file, "wb") as file:
        write_data = pickle.Pickler(file)
        write_data.dump(data)


def check_isfile(file):
    """on vérifie si le chromedriver existe dans le répertoire courant pour en connaître la version"""
    chrome_version = get_version()
    # print(f"la version de chrome est {chrome_version}")
    if os.path.isfile(file):
        version = check_driver()
        # print(f"la version du chromedriver est {version}")
        if version != chrome_version:
            get_driver(chrome_version)
            print("les versions divergent")
    else:
        get_driver(chrome_version)
        print("on télécharge le chromedriver correspondant à chrome parce qu'aucune version n'a été trouvée")


def get_version():
    """récupération du numéro de version du chrome local"""
    google_path = "C:/Program Files/Google/Chrome/Application"
    chrome_version = os.listdir(google_path)[0][:2]
    return chrome_version


def check_driver():
    with Chrome(executable_path="chromedriver.exe") as driver:
        if 'browserVersion' in driver.capabilities:
            return driver.capabilities['browserVersion'].split(".")[0]  # 92
        return driver.capabilities['version'].split(".")[0]


def get_driver(current_version):
    """on récupère la version du chromedriver compatible avec chrome"""
    # on fait une requête pour récupérer le numéro de version du dernier chromedriver
    url = "http://chromedriver.chromium.org/downloads"

    # on fetch l'url que l'on traite comme une string que l'on split à chaque fin de ligne (ici du JS, donc ";")
    response = requests.get(url).text.split(";")

    # on passe toutes les lignes en revue pour lister toutes les occurences d'une classe CSS
    target = 'class="XqQF9c"'
    link = [row for row in response if target in row]

    # on itère la liste pour trouver une correspondance avec le numéro de version actuel de chromium
    last_version = [row for row in link if current_version in row][0]

    # on crée une regex pour en rechercher la première occurence (l'url de la dernière version du chromedriver)
    regex = re.search("https://.+path=[0-9.]+/", last_version).group()
    print(f"le regex me renvoie {regex}")  # https://chromedriver.storage.googleapis.com/index.html?path=92.0.4515.107/

    # je relance une requête sur l'url regex, cette fois avec le module requests-html qui permet d'exécuter le code JS
    session = HTMLSession()
    response = session.get(regex)

    # on appelle la méthode render() afin d'exécuter le javascript de la page
    response.html.render(sleep=2, timeout=8)

    # on récupère le premier élément de la liste renvoyée par la méthode xpath()
    url = response.html.xpath("/html/body/table/tbody/tr[7]/td[2]/a")[0]

    # on extrait le href de l'élément précédent
    url = url.absolute_links

    # on convertit le set result en liste pour en extraire le premier élément
    url = list(url)[0]
    print(
        f"l'url de téléchargement est {url}"
    )  # https://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_win32.zip

    # on télécharge le fichier distant
    response = session.get(url)

    # on supprime l'ancienne version du chromedriver pour pouvoir accueillir la nouvelle sans conflit de namespace
    if os.path.isfile('chromedriver.exe'):
        os.remove('chromedriver.exe')
    else:
        print("fichier inexistant : impossible de supprimer 'chromedriver.exe")

    # on enregistre localement l'archive zippée
    save_datas('chromedriver.zip', response)

    # on extrait vers le répertoire courant le fichier chromedriver de l'archive zippée
    with ZipFile('chromedriver.zip', 'r') as zipped_file:
        zipped_file.extract('chromedriver.exe')

    # on supprime l'archive après l'extraction du fichier chromedriver.exe
    if os.path.isfile('chromedriver.zip'):
        os.remove('chromedriver.zip')
    else:
        print("fichier inexistant : impossible de supprimer 'chromedriver.zip")


def check_window(driver):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.ID, ""))
    driver.find_element_by_xpath('//*[@id="popin_tc_privacy_button"]').click()


"""
tout fonctionne jusqu'au contôle de la page courante, où l'ouverture de la seconde page n'est pas détéctée.
Il faut donc comprendre le fonctionnement de window_handle
"""