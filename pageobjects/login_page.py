from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class login_page:
    
    def __init__(self, driver):
        self.driver = driver
        self.emailField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'email')))
        self.pwField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
        self.loginStay = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="login"]//*[contains(text(),"이메일 주소 저장")]')))
        self.resetLink = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, '비밀번호 찾기')))
        self.loginBtn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@type="submit"]')))
        

    def validate_emailField_is_present(self):
        assert self.emailField.is_displayed()

    def validate_pwField_is_present(self):
        assert self.pwField.is_displayed()

    def validate_loginStay_is_present(self):
        assert self.loginStay.is_displayed()

    def validate_resetLink_is_present(self):
        assert self.resetLink.is_displayed()
    
    def validate_loginBtn_is_present(self):
        assert self.loginBtn.is_displayed()
    