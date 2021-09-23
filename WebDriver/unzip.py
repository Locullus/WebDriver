"""fichier de test pour la vesion JS où je rencontre des difficultés à dézipper le fichier reçu"""

from zipfile import ZipFile
import os

with open('chromedriverJS.zip', 'rb') as MyZip:
    print(MyZip.read(4))

with ZipFile('chromedriverJS.zip', 'r') as zipped_file:
    zipped_file.extract('chromedriverJS.exe')

# on supprime l'archive après l'extraction du fichier chromedriver.exe
if os.path.isfile('chromedriverJS.zip'):
    os.remove('chromedriverJS.zip')
else:
    print("fichier inexistant : impossible de supprimer 'chromedriverJS.zip")
