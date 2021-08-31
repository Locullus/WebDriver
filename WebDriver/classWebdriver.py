from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import SessionNotCreatedException
import time


class Webdriver:
    def __init__(self, url: str):
        self.url = url
        self.options = Options()
        self.options.headless = False
        self.options.page_load_strategy = 'normal'

        try:
            with Chrome(executable_path="chromedriver.exe", options=self.options) as self.driver:
                self.driver.implicitly_wait(2)
                self.driver.maximize_window()
                self.driver.get(self.url)
                assert "Python" in self.driver.title
                elem = self.driver.find_element_by_name("q")
                elem.clear()
                elem.send_keys("pycon")
                elem.send_keys(Keys.RETURN)
                assert "No results found." not in self.driver.page_source
                time.sleep(10)
                self.driver.close()
        except SessionNotCreatedException:
            print("problème avec la version actuelle du chromedriver...")
