import time
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.testproject.decorator import report
from pageobjects.login_page import login_page
from pageobjects.projectlist_page import ProjectlistPage
from pageobjects.home_page import HomePage
from webdriver import Driver
from tests.test_base import BaseTestCase
from utils.load_json import LoadJson


class TEST_Projectlist(BaseTestCase):

    def tearDown(self):
        self.driver.delete_all_cookies()

    def move_to_projectlist_page(self):

        try:
            homeScreen = HomePage(self.driver)
            homeScreen.gnb_project.click()
            time.sleep(1)
        except Exception as e:
            self.driver.report().step(description='Home page Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        

    @report(test='Projectlist Display Test')
    def test_projlist_display(self):
        self.move_to_projectlist_page()
        time.sleep(1)

        projectlist_page = ProjectlistPage(self.driver)
        try:

            projectlist_page.validate_projectlist_title_is_present()
            projectlist_page.validate_projectlist_compfilter_is_present()
            projectlist_page.validate_projectlist_nomemberfilter_is_present()
            projectlist_page.validate_projectlist_periodfilter_is_present()
            projectlist_page.validate_projectlist_tagfilter_is_present()
            projectlist_page.validate_projectlist_projcreateButton_is_present()
                    
            self.assertEqual(self.driver.current_url.split('/')[3], 'projectList', "The page is not on the Projectlist") # assert if the projectlist page url has 'projectlist'
            self.assertTrue(projectlist_page.projectlist_title.text.__contains__('프로젝트')) # assert if the title of projectlist page has '프로젝트'                    
            self.assertEqual(projectlist_page.projectlist_title.text.split('(')[1].split(')')[0],str(len(projectlist_page.projectlist_list))) # assert if the number of project list is shown in the title

        except Exception as e:
            self.driver.report().step(description='Projectlist display Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)

    @report(test='Projectlist period filter Test')
    def test_projectlist_period_filter(self):
        # 일정 필터 테스트
        projectlist_page = ProjectlistPage(self.driver)
        try:            
            # 캘린더 열기
            projectlist_page.projectlist_periodfilter.click()
            time.sleep(3)

            # 연도 값 클릭
            period_year = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[contains(@class, "q-date__navigation")]/div[contains(@class,"relative-position")][2]//*[contains(@class,"q-btn__content")]')))
            period_year.click()

            # 올해의 연도 선택
            period_current_year = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "q-date__today")))
            period_current_year.click()

            # 월 값 클릭
            period_month = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[contains(@class, "q-date__navigation")]/div[contains(@class,"relative-position")][1]')))
            period_month.click()

            # 이번 달 선택
            period_current_month = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "q-date__today")))
            period_current_month.click()
            time.sleep(3)

            # 이번 달 일정 전체 선택. 처음 클릭 시 기본 선택 값(앞/뒤 3개월씩) 해제
            self.driver.find_element_by_xpath('//*[contains(@class,"q-date__calendar-item--in")][1]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[contains(@class,"q-date__calendar-item--in")][1]').click()
            # 이번 달의 마지막 날짜 클릭
            days = self.driver.find_elements_by_xpath('//*[contains(@class,"q-date__calendar-item--in")]')
            max_days = len(days)            
            days[max_days-1].click()
            
            time.sleep(3)
            self.driver.find_element_by_xpath('//*[contains(@class, "q-date__actions")]//*[contains(text(),"확인")]').click()

            time.sleep(3)

        except Exception as e:
            self.driver.report().step(description='Projectlist period filter Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)

        finally:
            time.sleep(1)
    
    @report(test="Finalize Projectlist")
    def test_finalize_projectlist(self):     
        self.driver.get(self.base_url)
        self.assertEqual(self.driver.current_url, self.base_url)


if __name__ == "__main__":
    unittest.main()

