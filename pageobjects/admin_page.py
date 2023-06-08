from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class admin_page:
    
    def __init__(self, driver):
        self.driver = driver
        self.globalBtns = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'global-nav')))
        self.adminBtn = self.globalBtns[3]
        self.menuBtns = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'admin-btn')))
        self.msgBtn = self.menuBtns[0]
        self.userBtn = self.menuBtns[1]
        self.corpBtn = self.menuBtns[2]
        self.depBtn = self.menuBtns[3]
        self.roleBtn = self.menuBtns[4]
        self.codeBtn = self.menuBtns[5]

        
