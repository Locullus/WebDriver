import os
import re
import pickle
import requests
import selenium.common.exceptions
from requests_html import HTMLSession
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from zipfile import ZipFile


def save_datas(my_file, data):

    """ fonction qui enregistre les données dans un fichier externe """

    with open(my_file, "wb") as file:
        write_data = pickle.Pickler(file)
        write_data.dump(data)


def get_datas(my_file):
    """ fonction qui récupère les données d'un fichier s'il existe et qui le crée sinon """
    try:
        with open(my_file, "rb") as file:
            get_data = pickle.Unpickler(file)
            return get_data.load()

    except (FileNotFoundError, EOFError):   # EOFError concerne les fichiers existants mais vides
        print("ce fichier n'existe pas")
        return None


def check_isfile(file):

    """on vérifie si le chromedriver existe dans le répertoire courant pour en connaître la version"""

    chrome_version = get_version()
    print(f"la version de chrome est {chrome_version}")

    # si le fichier existe :
    if os.path.isfile(file):

        # on vérifie si son numéro de version est enregistré
        version = get_datas('chromedriver_version')

        # s'il ne l'est pas :
        if version is None:

            # on lance le chromedriver pour récupérer son numéro de version
            version = check_driver()
            print(f"la version du chromedriver est {version}")

            # on enregistre le numéro de version dans le fichier dédié
            save_datas('chromedriver_version', version)
            print("sauvegarde dans le fichier chromedriver_version")

        # si les versions diffèrent :
        if version != chrome_version:

            # on lance un update du chromedriver
            get_driver(chrome_version)
            print("les versions divergent")

    # si le fichier n'existe pas on lance un update du chromedriver
    else:
        get_driver(chrome_version)
        print("on télécharge le chromedriver correspondant à chrome parce qu'aucune version n'a été trouvée")


def get_version():

    """récupération du numéro de version du chrome local"""

    # je spécifie 2 chemins d'accès possible pour chrome
    google_path = "C:/Program Files/Google/Chrome/Application"
    google_path2 = "C:/Program Files (x86)/Google/Chrome/Application"

    # si le premier chemin échoue, on essaie le second
    try:
        return os.listdir(google_path)[0][:2]
    except FileNotFoundError:
        try:
            return os.listdir(google_path2)[0][:2]
        except FileNotFoundError:
            print("impossible de trouver le chemin d'accès à chrome")


def check_driver():
    try:
        with Chrome(executable_path="chromedriver.exe") as driver:
            if 'browserVersion' in driver.capabilities:
                return driver.capabilities['browserVersion'].split(".")[0]  # 92
            return driver.capabilities['version'].split(".")[0]
    except selenium.common.exceptions.SessionNotCreatedException:
        print("problème avec le chromedriver.")


def get_driver(current_version):

    """on récupère la version du chromedriver compatible avec chrome"""

    # on fait une requête pour récupérer le numéro de version du dernier chromedriver
    url = "http://chromedriver.chromium.org/downloads"

    # on fetch l'url que l'on traite comme une string que l'on split à chaque fin de ligne (ici du JS, donc ";")
    response = requests.get(url).text.split(";")

    # on passe toutes les lignes en revue pour lister toutes les occurences d'une classe CSS
    target = 'class="XqQF9c"'
    link = [row for row in response if target in row]

    # on crée une regex pour s'assurer que ce que l'on récupère est bien un numéro de version
    regex_version = re.compile(r"\s" + current_version + r"\.[0-9]\.[0-9]{4}\.[0-9]+")

    # on itère la liste pour trouver une correspondance avec le numéro de version actuel de chromium
    last_version = [row for row in link if re.search(regex_version, row) is not None][0]

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

    # on enregistre le nouveau numéro de version dans le fichier dédié
    save_datas('chromedriver_version', current_version)
    print("sauvegarde dans le fichier chromedriver_version")


def browser(headless: bool = False):

    """fonction qui configure le driver en mode headless ou visible et qui fournit le path"""

    options = Options()
    options.headless = headless  # configuration du driver en mode visible ou headless
    options.page_load_strategy = 'normal'
    return Chrome(executable_path="chromedriver.exe", options=options)


def close_pop_up(driver):

    """ on attend l'apparition de la fenêtre des cookies pour la fermer"""

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'popin_tc_privacy_button'))).click()
    except selenium.common.exceptions.WebDriverException as e:
        print(e)
