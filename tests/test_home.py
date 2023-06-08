import unittest
from src.testproject.decorator import report
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time
from values import strings
from webdriver import Driver
from pageobjects.home_page import HomePage
from pageobjects.common_objects import common_objects
import sys
from tests.test_base import BaseTestCase

class Test_home(BaseTestCase):

    def tearDown(self):
        self.driver.delete_all_cookies()

    @report(test='Display Check')
    def test_displayCheck(self):
        try:
            homepage = HomePage(self.driver)
            # title, gnb, lnb 정상 표시되는지 확인

            homepage.validate_tab_title()
            # home active 확인
            assert 'active' in homepage.gnb_home.get_attribute("class")
            homepage.validate_gnb_home_is_present()
            homepage.validate_gnb_project_is_present()
            homepage.validate_gnb_schedule_is_present()
            homepage.validate_gnb_report_is_present()
            homepage.validate_home_elements()

        except Exception as e:
            self.driver.report().step(description='Display Check Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)
    
    @report(test='Move to Project Page')
    def move_to_project_page(self):
        try:
            homepage = HomePage(self.driver)
            homepage.gnb_project.click()
            time.sleep(1)
            assert 'projectList' in self.driver.current_url
        except Exception as e:
            self.driver.report().step(description='Move to Project Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        else:
            homepage.gnb_home.click()

    @report(test='Move to Schedule Page')
    def move_to_schedule_page(self):
        try:
            homepage = HomePage(self.driver)
            homepage.gnb_schedule.click()
            time.sleep(1)
            assert 'schedule' in self.driver.current_url
        except Exception as e:
            self.driver.report().step(description='Move to Schedule Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        else:
            homepage.gnb_home.click()            

    @report(test='Move to Report Page')
    def move_to_report_page(self):
        try:
            homepage = HomePage(self.driver)
            homepage.gnb_report.click()
            time.sleep(1)
            assert 'report' in self.driver.current_url
        except Exception as e:
            self.driver.report().step(description='Move to Report Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        else:
            homepage.gnb_home.click()            
    
    @report(test='Move to Contact Admin Page')
    def move_to_contact_admin_page(self):
        try:
            homepage = HomePage(self.driver)
            homepage.contact_admin.click()
            time.sleep(2)
            # self.driver.switch_to.window(self.driver.window_handles[1])
            assert 'bbsadmin' in self.driver.current_url
        except Exception as e:
            self.driver.report().step(description='Move to Contact Admin Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        else:
            # self.driver.close()
            # self.driver.switch_to.window(self.driver.window_handles[0])
            homepage.gnb_home.click()

    @report(test='Move to Guide')
    def move_to_guide_page(self):
        try:
            homepage = HomePage(self.driver)
            homepage.guide.click()
            time.sleep(5)
            self.driver.switch_to.window(self.driver.window_handles[1])
            assert 'help' in self.driver.current_url
        except Exception as e:
            self.driver.report().step(description='Move to Guide Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        else:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])    

    @report(test='Move to Notice Page')
    def move_to_notice_page(self):
        try:
            homepage = HomePage(self.driver)
            homepage.notice.click()
            time.sleep(2)
            assert 'bbsNotice' in self.driver.current_url
        except Exception as e:
            self.driver.report().step(description='Move to Notice Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        else:
            homepage.gnb_home.click()

    @report(test='Move to Customer Service Page')
    def move_to_cs_page(self):
        try:
            homepage = HomePage(self.driver)
            homepage.customer_service.click()
            time.sleep(2)
            assert 'bbsQna' in self.driver.current_url
        except Exception as e:
            self.driver.report().step(description='Move to bbsQna Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        else:
            homepage.gnb_home.click()

    @report(test='Project Card Test')
    def test_project_card(self):
        try:
            time.sleep(2)
            proj_card = self.driver.find_elements_by_class_name("projbox")
            proj_name = proj_card[0].find_element_by_class_name("title")
            proj_name_xpath = '//*[@id="app"]//*[contains(text(), "' + proj_name.text+ '")]'
            proj_name.click()      

            time.sleep(2)                
            assert 'project' in self.driver.current_url
            validate_title = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, proj_name_xpath)))
            assert  len(validate_title) >= 2
            assert 'active' in self.driver.find_element_by_id("Project").get_attribute("class")
        except Exception as e:
            self.driver.report().step(description='Project Card Test Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        else:
            self.driver.find_element_by_id("Home").click()

    @report(test='Project Create Test')            
    def move_to_project_create(self):
        try:
            self.driver.find_element_by_xpath('//*[@role="button"]//*[contains(text(), "프로젝트 생성")]').click()
            time.sleep(2)
            assert 'createProject' in self.driver.current_url
            assert 'active' in self.driver.find_element_by_id("Project").get_attribute("class")

        except Exception as e:
            self.driver.report().step(description='Move to Project Create Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
    
    @report(test='Validate Project in Home')            
    def validate_project_in_home(self):
        try:
            time.sleep(3)
            #프로젝트제목, 기간 정보 가져오기
            proj_name = self.driver.find_element_by_xpath('//*[@class="proj-detail"]//*[contains(text(), "Automation")]').text
            proj_period = self.driver.find_element_by_xpath('//*[@class="group"]//*[contains(text(), "21")]').text
            #홈으로 이동
            self.driver.find_element_by_id("Home").click()
            time.sleep(2)
            #홈에서 모든 카드 정보 가져오기
            proj_cards = self.driver.find_elements_by_class_name("projbox")
            
            #카드 정보에 생성한 프로젝트 정보 있는지 확인
            for proj_card in proj_cards :
                flag = False
                if proj_name == proj_card.find_element_by_class_name("title").text :
                    if proj_period == proj_card.find_element_by_class_name("date").text :
                        flag = True
                        break
            
            assert flag
            
        except Exception as e:
            self.driver.report().step(description='Validate Project in Home Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        
