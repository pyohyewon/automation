from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class common_objects:

    def __init__(self, driver):
        self.driver = driver

    def find_popupBox(self):
        self.popup = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'popup-alarm-box')))
        


        return self.popup