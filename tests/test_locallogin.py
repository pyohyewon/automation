import unittest
from src.testproject.decorator import report
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time

from pageobjects.login_page import login_page
import sys
from tests.test_base import BaseTestCase
from values import strings
from webdriver import Driver
from tests.test_base import BaseTestCase

class Test_Local_login(BaseTestCase):

    common = None


    @classmethod
    def setUpClass(cls):
        cls.driver.get(strings.base_url)
    #    cls.common = Driver(testjobname='Login Test')
    #    cls.driver = cls.common.instance

    # Test Condition Setting
    #def setUp(self):
    #    self.driver.get(strings.base_url)


    def tearDown(self):
        self.driver.delete_all_cookies()

    @report(test='Display Check')
    def test_displayCheck(self):
        try:

            loginpage = login_page(self.driver)
            #id, pw, checkbox, btn 정상 표시되는지 확인
            loginpage.validate_emailField_is_present()
            loginpage.validate_pwField_is_present()
            loginpage.validate_loginStay_is_present()
            loginpage.validate_resetLink_is_present()
            loginpage.validate_loginBtn_is_present()

        except Exception as e:
            self.driver.report().step(description='display Check Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)
            

    @report(test='Normal Login Test')
    def test_login(self): 
        try:

            loginpage = login_page(self.driver)

            # 정상 Login sequence (Login 후 Logout 버튼이 존재하면 Pass)
            loginpage.emailField.clear()
            loginpage.emailField.send_keys(strings.userEmail)
            loginpage.pwField.clear()
            loginpage.pwField.send_keys(strings.userPw)
            
            loginpage.loginBtn.click()
            time.sleep(1)

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gnb"]//*[contains(text(),"홈")]')))


        except Exception as e:
            self.driver.report().step(description='Normal Login Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)
        
    @report(test='Logout Test')
    def test_logout(self): 
        try:
            
            # 정상 Logout sequence (Logout 후 Login 버튼이 존재하면 Pass)
            self.driver.find_element_by_xpath('//*[@id="gnb"]//*[contains(text(),"Korens")]').click() 
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gnb"]//*[contains(text(),"로그아웃")]'))).click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'login')))
            time.sleep(1)

        except Exception as e:
            self.driver.report().step(description='Logout Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)
        

            

    @report(test='Blank ID Test')
    def test_blankID(self):   
        # blank id check (Login 시도 후 안내메세지 일치하면 Pass)
        try:

            loginpage = login_page(self.driver)
            loginpage.emailField.send_keys(Keys.CONTROL,"a")
            loginpage.emailField.send_keys(Keys.DELETE)
            
            #loginpage.emailField.clear()
            #loginpage.pwField.clear()
            
            time.sleep(1)
            
            loginpage.loginBtn.click()
            time.sleep(1)

            popup_box = self.driver.find_element_by_class_name('popup-alarm-box')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]//*[contains(text(),"아이디를 입력해주세요.")]')))
            #WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="app"]/div[2]/div[2]/div/div/div[2]/div'), "아이디을/를 입력해주세요."))
            
        except Exception as e:
            self.driver.report().step(description='Blank ID Test Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)
            pass
       
        else:
            self.driver.find_element_by_xpath('//*[@id="app"]//*[contains(text(),"확인")]').click()

            time.sleep(2)
        


    @report(test='Blank Password Test')
    def test_blankPW(self):
        # blank password check
        try:

            loginpage = login_page(self.driver)
            loginpage.emailField.clear()
            loginpage.emailField.send_keys(strings.userEmail)
            loginpage.pwField.send_keys(Keys.CONTROL,"a")
            loginpage.pwField.send_keys(Keys.DELETE)
            #loginpage.pwField.clear()
            
            time.sleep(1)
            
            loginpage.loginBtn.click()
            time.sleep(1)
            #self.driver.find_element_by_class_name('popup-box').is_displayed()
            #WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="app"]/div[2]/div[2]/div/div/div[2]/div'), "패스워드을/를 입력해주세요."))
            popup_box = self.driver.find_element_by_class_name('popup-alarm-box')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]//*[contains(text(),"패스워드를 입력해주세요.")]')))

        except Exception as e:
            self.driver.report().step(description='Blank Password Test Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)
            pass
        else:
            self.driver.find_element_by_xpath('//*[@id="app"]//*[contains(text(),"확인")]').click()
            #self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div/div[3]/div').click()
            time.sleep(2)

    @report(test='Abnormal Login Test')
    def test_abnormalLogin(self):
        try:

            loginpage = login_page(self.driver)
            loginpage.emailField.clear()
            loginpage.emailField.send_keys(strings.userEmail)
            loginpage.pwField.clear()
            loginpage.pwField.send_keys(' ')

            loginpage.loginBtn.click()
            time.sleep(1)
            #self.driver.find_element_by_class_name('popup-box').is_displayed()
            #WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="app"]/div[2]/div[2]/div/div/div[2]/div'), "존재하지 않는 사용자 입니다. 아이디/패스워드 확인 해주세요!."))
            popup_box = self.driver.find_element_by_class_name('popup-alarm-box')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]//*[contains(text(),"로그인에 실패하였습니다.")]')))

        except Exception as e:
            self.driver.report().step(description='Abnormal Login Test Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)
            pass
        else:
            #self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div/div[3]/div').click()
            self.driver.find_element_by_xpath('//*[@id="app"]//*[contains(text(),"확인")]').click()
            time.sleep(2)
                    
if __name__ == "__main__":
    unittest.main()