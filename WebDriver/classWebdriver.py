from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException
import time


class Webdriver:
    def __init__(self, url):
        self.url = url
        self.options = Options()
        self.options.headless = False
        self.options.page_load_strategy = 'normal'

        try:
            with Chrome(executable_path="chromedriver.exe", options=self.options) as self.driver:
                self.driver.implicitly_wait(2)
                self.driver.maximize_window()
                self.driver.get(self.url)
                time.sleep(10)
        except SessionNotCreatedException:
            print("problème avec la version actuelle du chromedriver...")
