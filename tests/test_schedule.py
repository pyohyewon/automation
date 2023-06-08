from datetime import datetime
from src.testproject.decorator import report
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pageobjects.schedule_page import SchedulePage
from tests.test_base import BaseTestCase
from utils.load_json import LoadJson

class Test_schedule(BaseTestCase):

    defined_statuslist = LoadJson.json_predefined_data.get('bookmark_statuslist')
    
    def tearDown(self):
        self.driver.delete_all_cookies()

    @report(test='Display Check')
    def test_displayCheck(self):
        try:
            # GNB에서 Schedule 메뉴 선택
            self.driver.find_element_by_id("Schedule").click()
            time.sleep(2)
            schedule_page = SchedulePage(self.driver)
            # objects 정상 표시되는지 확인
            schedule_page.validate_ganttList_is_present()
            schedule_page.validate_ganttBars_is_present()
            schedule_page.validate_sortList_is_present()
            schedule_page.validate_projectFilter_is_present()
            schedule_page.validate_tagFilter_is_present()
            schedule_page.validate_calendar_is_present()
            schedule_page.validate_statusFilter_is_present()
            schedule_page.validate_bookmarkFilter_is_present()
            schedule_page.validate_zoomin_is_present()
            schedule_page.validate_zoomout_is_present()
            schedule_page.validate_dayFilter_is_present()
            schedule_page.validate_weekFilter_is_present()
            schedule_page.validate_monthFilter_is_present()
            schedule_page.validate_quarterFilter_is_present()
            schedule_page.validate_foldUnfoldBtn_is_present()
            schedule_page.validate_projCreate_is_present()
            schedule_page.validate_gridFoldBtn_is_present()


        except Exception as e:
            self.driver.report().step(description='Display Check Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)

    @report(test='Chart Sorting Check')
    def test_chart_sorting(self):
        try:
            schedule_page = SchedulePage(self.driver)
            # 정렬 확인을 위해 세부 정보 펼치기
            schedule_page.gridFoldBtn.click()
            schedule_page.foldUnfoldBtn = schedule_page.validate_foldUnfoldBtn_is_present()
            if schedule_page.foldUnfoldBtn.text == 'keyboard_arrow_up':
                schedule_page.foldUnfoldBtn.click()            

            # 종료일순, 시작일순, 이름순
            for i in range(0, 3):
                schedule_page.sortList.click()
                selectbox = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="list"]//*')))
                selectbox[i].click()
                time.sleep(3)
                if i == 0 :
                    itemList = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'project-end-date')))
                elif i == 1:
                    itemList = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'project-start-date')))
                elif i == 2:
                    itemList = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'content-title')))
                textArr = []
                for idx in range(len(itemList)) :
                   # dateArr.append(time.strptime(dateList[idx].text, "'%y.%m.%d."))
                   textArr.append(itemList[idx].text)
                assert sorted(textArr) == textArr
            # 상태순
            schedule_page.statusFilter.click()
            schedule_page.sortList.click()
            selectbox = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="list"]//*')))
            selectbox[3].click()
            itemList = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'project-status')))
            sortArr = []
            for idx in range(len(itemList)) :
                sortArr.append(self.defined_statuslist.index(itemList[idx].text))
            assert sorted(sortArr) == sortArr

        except Exception as e:
            self.driver.report().step(description='Chart Sorting Check Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)            

    @report(test='Project filter Check')
    def test_project_filtering(self):
        try:
            schedule_page = SchedulePage(self.driver)
            schedule_page.projectFilter.click()
            project = self.driver.find_element_by_css_selector('div[class*="tag-select-list"] label[class="custom-check"]')
            project_name = project.text
            project.click()
            self.driver.find_element_by_xpath('//*[@class="btn-arry-right"]//*[contains(text(),"적용")]').click()
            assert project_name == self.driver.find_element_by_class_name('content-title').text
        
        except Exception as e:
            self.driver.report().step(description='Chart Sorting Check Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)                        
        
        finally:            
            schedule_page.projectFilter.click()
            self.driver.find_element_by_xpath('//*[@class="btn-arry-right"]//*[contains(text(),"초기화")]').click()
            self.driver.find_element_by_xpath('//*[@class="btn-arry-right"]//*[contains(text(),"적용")]').click()

    @report(test='Schedule Bar Adjust Check')
    def test_scheduleBarAdjust(self):
        
        #일정관리 화면 elements
        schedule_page = SchedulePage(self.driver)
        
        schedule_page.validate_ganttList_is_present()
        schedule_page.validate_ganttBars_is_present()
        #gantt list 가져오기
        ganttLists = schedule_page.find_ganttList()
        startOriginDate = ganttLists[0].find_element_by_css_selector("div[data-column-name='start_date']").text
        
        schedule_page.ganttBars[0].click()
        dragSource = self.driver.find_element_by_xpath('//*[@id="gantt_here"]/div/div[1]/div[3]/div/div/div[2]/div[3]/div[1]/div[4]')
        time.sleep(1)
        
        #Bar Drag
        ActionChains(self.driver).drag_and_drop_by_offset(dragSource, 800, 0).perform()
        #ActionChains(self.driver).move_to_element(schedulepage.ganttBars[0]).move_by_offset()
        #ActionChains(self.driver).click_and_hold(dragSource).move_by_offset(800, 0).release().perform()
        
        ganttLists = schedule_page.find_ganttList()
        
        startChangeDate = ganttLists[0].find_element_by_css_selector("div[data-column-name='start_date']").text

        if startOriginDate != startChangeDate:
            print("Success: Gantt Bar was changed!")
            
        else:
            print("Fail: Gantt Bar didn't be changed.")

        assert startOriginDate != startChangeDate
        
        time.sleep(3)

    @report(test='Schedule Popup Check')
    def test_schedulePopup(self):
        
        #일정관리 화면 elements
        schedule_page = SchedulePage.schedule_page(self.driver)
        
        schedule_page.validate_ganttList_is_present()
        schedule_page.validate_ganttBars_is_present()
        #gantt list 가져오기
        ganttLists = schedule_page.find_ganttList()
        startOriginDate = ganttLists[0].find_element_by_css_selector("div[data-column-name='start_date']").text
        
        schedule_page.ganttBars[0].click()
        dragSource = self.driver.find_element_by_xpath('//*[@id="gantt_here"]/div/div[1]/div[3]/div/div/div[2]/div[3]/div[1]/div[4]')
        time.sleep(1)
        
        #Bar Drag
        ActionChains(self.driver).drag_and_drop_by_offset(dragSource, 800, 0).perform()
        #ActionChains(self.driver).move_to_element(schedulepage.ganttBars[0]).move_by_offset()
        #ActionChains(self.driver).click_and_hold(dragSource).move_by_offset(800, 0).release().perform()
        
        ganttLists = schedule_page.find_ganttList()
        
        startChangeDate = ganttLists[0].find_element_by_css_selector("div[data-column-name='start_date']").text

        if startOriginDate != startChangeDate:
            print("Success: Gantt Bar was changed!")
            
        else:
            print("Fail: Gantt Bar didn't be changed.")

        assert startOriginDate != startChangeDate
        
        time.sleep(3)

