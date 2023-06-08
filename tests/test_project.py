from src.testproject.decorator import report
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time
from pageobjects.project_page import project_page
from pageobjects.common_objects import common_objects
import sys
from tests.test_base import BaseTestCase

class Test_project(BaseTestCase):

    # Test Condition Setting
    #def setUp(self):
    #    self.driver.get()

    def tearDown(self):
        self.driver.delete_all_cookies()

    @report(test='Display Check')
    def test_displayCheck(self):
        try:
            # GNB에서 Project 메뉴 선택
            self.driver.find_element_by_id("Project").click()
            if 'projectList' not in self.driver.current_url:
                self.driver.find_element_by_xpath('//*[@class="group"]//*[contains(text(),"← 프로젝트 리스트")]').click()
            # 프로젝트 생성 버튼 클릭
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@role="button"]//*[contains(text(),"프로젝트 생성")]'))).click()
    
            assert 'createProject' in self.driver.current_url

            time.sleep(2)
            project_create_page = project_page()
            # 입력 필드 정상 표시되는지 확인
            project_create_page.find_main_objects(self.driver)
            project_create_page.validate_title_is_present()
            project_create_page.validate_expectedEnd_is_present()
            project_create_page.validate_cancel_is_present()
            project_create_page.validate_save_is_present()
            project_create_page.validate_leader_name()

        except Exception as e:
            self.driver.report().step(description='Display Check Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)
    
    @report(test='Project Create')
    def test_projectCreate(self):
        try:
            project_create_page = project_page()
            project_create_page.find_main_objects(self.driver)
            # 프로젝트 생성 필수값 입력
            title_str = 'Automation ' + time.strftime('%m%d%H%M%S', time.localtime(time.time()))
            project_create_page.title.send_keys(title_str)
            project_create_page.expectedEnd.click()
            time.sleep(2)
            calendar = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'q-date__calendar-item--in')))
            
            calendar[len(calendar) - 1].click()
            time.sleep(1)
            project_create_page.save.click()
            time.sleep(2)
            
            #생성된 값 개요에서 확인
            proj_name_xpath = '//*[@id="app"]//*[contains(text(), "' + title_str + '")]'
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, proj_name_xpath)))

            #프로젝트 리스트에서 확인
            self.driver.find_element_by_xpath('//*[@class="group"]//*[contains(text(),"← 프로젝트 리스트")]').click()
            project_list = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="divTable"]//*[@class="subject"]')))
            assert project_list[0].text == title_str

            project_list[0].click()

        except Exception as e:
            self.driver.report().step(description='Project Create Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)
  
    @report(test='Project Modify')
    def test_projectModify(self):
        try:
            # 프로젝트 수정 버튼 클릭
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="proj-detail"]//*[contains(text(),"수정")]'))).click()
            time.sleep(2)
            project_modify_page = project_page()
            project_modify_page.find_main_modify_objects(self.driver)
            project_modify_page.title.send_keys(" 수정")
            
            # 관리부서 추가 버튼 클릭
            project_modify_page.add_dept_btn.click()
            dept_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="q-tree"]/div/div[1]')))
            dept_name = dept_element.find_element_by_class_name('part-name').text
            dept_element.find_element_by_xpath('*[@role="checkbox"]').click()
            self.driver.find_element_by_xpath('//*[@role="button"]//*[contains(text(),"확인")]').click()
            
            # 설명 입력
            project_modify_page.explain.send_keys("수정")

            # 태그 입력
            project_modify_page.tag.send_keys("수정")
            project_modify_page.tag.send_keys(Keys.ENTER)
            
            # 마일스톤 입력
            project_modify_page.mst_name.send_keys("수정")
            project_modify_page.mst_date.click()
            calendar = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'q-date__calendar-item--in')))
            calendar[0].click()
            self.driver.find_element_by_xpath('//*[@role="button"]//*[text()="추가"]').click()
            
            # 저장 버튼 클릭
            project_modify_page.save.click()
            
            # 팝업 박스 확인
            popupBox = common_objects(self.driver).find_popupBox()
            assert "저장" in popupBox.find_element_by_xpath('div/div[2]/div').text, '실패'
            popupBox.find_element_by_xpath('div/div[3]/div').click()
            
            # 수정된 정보 확인 (제목/관리부서/설명/태그/마일스톤)
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//*[@class="bgico-sm-main"]'), '수정'))
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//*[@class="rpsv"]'), dept_name))
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//*[@class="txt-pre explan"]'), '수정'))
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//*[@class="tag mr4"]/span'), '수정'))
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//label'), '수정'))

        except Exception as e:
            self.driver.report().step(description='Project Modify Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)

    @report(test='Sub Project Create')
    def test_subCreate(self):
        try:
            # 하위항목 추가 버튼 클릭
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@class="project-information-box"]//*[contains(text(), "하위항목 추가")]'))).click()
            # 하위 프로젝트 생성 버튼 클릭
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@class="drop-list on"]//*[contains(text(), "하위 프로젝트 생성")]'))).click()
            sub_create_page = project_page()
            sub_create_page.find_sub_objects(self.driver)
            # 하위 프로젝트 생성 필수값 입력
            title_str = 'Sub ' + time.strftime('%m%d%H%M%S', time.localtime(time.time()))
            sub_create_page.title.send_keys(title_str)
            sub_create_page.expectedEnd.click()
            time.sleep(2)
            calendar = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'q-date__calendar-item--in')))
            calendar[len(calendar) - 1].click()
            sub_create_page.save.click()
            time.sleep(2)
            # 생성된 값 개요 화면에서 확인
            sub_item_list = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'subject-title')))
            self.assertIn(title_str, sub_item_list[0].text)

            #WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="app"]/div/main/div[2]/div/div[3]/div/div/div[1]/div/div[1]/div[1]/span'), title_str))
        except Exception as e:
            self.driver.report().step(description='Sub Create Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)


    @report(test='Sub Project Modify')
    def test_subModify(self):
        try:
            # 하위 프로젝트 수정 버튼 클릭
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"수정")]'))).click()
            time.sleep(2)
            sub_modify_page = project_page()
            sub_modify_page.find_sub_objects(self.driver)
            sub_modify_page.title.send_keys(" 수정")
                       
            # 설명 입력
            sub_modify_page.explain.send_keys("수정")

            # 태그 입력
            sub_modify_page.tag.send_keys("수정")
            sub_modify_page.tag.send_keys(Keys.ENTER)
            
            # 이전 업무 선택
            sub_modify_page.pre_task.click()
            enabled_tasks = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[name=projectSelection]:not([disabled])')))
            pre_task_name = enabled_tasks[0].find_element_by_xpath('../..//*[@class="pl15 ellipsis title"]').text
            enabled_tasks[0].click()
            self.driver.find_element_by_xpath('//*[@class="popup"]//*[contains(text(), "확인")]').click()

            # 마일스톤 입력
            sub_modify_page.mst_name.send_keys("수정")
            sub_modify_page.mst_date.click()
            calendar = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'q-date__calendar-item--in')))
            calendar[0].click()
            self.driver.find_element_by_xpath('//*[@role="button"]//*[text()="추가"]').click()
            
            # 저장 버튼 클릭
            sub_modify_page.save.click()
            
            # 팝업 박스 확인
            popupBox = common_objects(self.driver).find_popupBox()
            assert "저장" in popupBox.find_element_by_xpath('div/div[2]/div').text, '실패'
            popupBox.find_element_by_xpath('div/div[3]/div').click()
            
            # 수정된 정보 확인 (제목/설명/태그/이전 업무/마일스톤)
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//*[@class="bgico-sm-sub"]'), '수정'))
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//*[@class="txt-pre explan"]'), '수정'))
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//*[@class="tag mr4"]/span'), '수정'))
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//*[@class="bgico-ti-sub"]'), pre_task_name))
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//label'), '수정'))

        except Exception as e:
            self.driver.report().step(description='Project Modify Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)

    @report(test='Task Create')
    def test_taskCreate(self):
        try:
            # 하위항목 추가 버튼 클릭
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@class="project-information-box"]//*[contains(text(), "하위항목 추가")]'))).click()
            # 태스크 생성 버튼 클릭
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@class="drop-list on"]//*[contains(text(), "태스크 생성")]'))).click()
            task_create_page = project_page()
            task_create_page.find_task_objects(self.driver)
            # 태스크 생성 필수값 입력
            title_str = 'Task ' + time.strftime('%m%d%H%M%S', time.localtime(time.time()))
            task_create_page.title.send_keys(title_str)
            task_create_page.expectedEnd.click()
            time.sleep(2)
            calendar = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'q-date__calendar-item--in')))
            calendar[len(calendar) - 1].click()
            task_create_page.save.click()
            time.sleep(2)
            # 생성된 값 개요 화면에서 확인
            task_item_list = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'subject-title')))
            flag = False
            # 하위 업무들 중 생성한 태스크가 존재하는지 확인
            for item in task_item_list:
                if title_str in item.text:
                    flag = True
                    break
            
            assert flag == True

        except Exception as e:
            self.driver.report().step(description='Task Create Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)

    @report(test='Task Modify')
    def test_taskModify(self):
        try:
            # 태스크 수정 버튼 클릭
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"수정")]'))).click()
            time.sleep(2)
            task_modify_page = project_page()
            task_modify_page.find_task_objects(self.driver)
            task_modify_page.title.send_keys(" 수정")

            # 태그 입력
            task_modify_page.tag.send_keys("수정")
            task_modify_page.tag.send_keys(Keys.ENTER)
            
            # 다음 업무 선택
            task_modify_page.next_task.click()
            enabled_tasks = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[name=projectSelection]:not([disabled])')))
            next_task_name = enabled_tasks[0].find_element_by_xpath('../..//*[@class="pl15 ellipsis title"]').text
            enabled_tasks[0].click()
            self.driver.find_element_by_xpath('//*[@class="popup"]//*[contains(text(), "확인")]').click()
            
            # 저장 버튼 클릭
            task_modify_page.save.click()
            
            # 팝업 박스 확인
            popupBox = common_objects(self.driver).find_popupBox()
            assert "저장" in popupBox.find_element_by_xpath('div/div[2]/div').text, '실패'
            popupBox.find_element_by_xpath('div/div[3]/div').click()
            
            # 태스크 상세 정보 펼치기
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@role="button"]//*[contains(text(), "keyboard_arrow_down")]'))).click()
            # 수정된 정보 확인 (제목/태그/다음 업무)
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//*[@class="bgico-sm-task"]'), '수정'))
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//*[@class="tag mr4"]/span'), '수정'))
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="proj-detail"]//*[@class="bgico-ti-sub"]'), next_task_name))

        except Exception as e:
            self.driver.report().step(description='Project Modify Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)

    def loop_projectDelete(self):
        # today = time.strftime("%m%d", time.localtime())
        project_list = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="divTable"]//*[@class="subject"]')))
        for project in project_list :
            # if "Automation " + today in project.text:
            if "Automation " in project.text:
                project.click()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(), "more_horiz")]'))).click()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class = "bgico-ti-del"]'))).click()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="popup-alarm"]//*[contains(text(), "확인")]'))).click()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="popup-alarm"]//*[contains(text(), "확인")]'))).click()
                return 1
        return 0

    @report(test='All Project Delete')
    def test_allProjectDelete(self):
        try:

            # 프로젝트 클릭 후 개요 화면이면, 리스트 버튼 클릭
            self.driver.find_element_by_id("Project").click()
            if 'projectList' not in self.driver.current_url:
                self.driver.find_element_by_xpath('//*[@class="group"]//*[contains(text(),"← 프로젝트 리스트")]').click()

            continue_yn = 1
            while continue_yn ==1 :
                continue_yn = self.loop_projectDelete() 
                


        except Exception as e:
            self.driver.report().step(description='Project Modify Exception', message='Occurred Exception'+str(e), passed=False, pageshot=True)            
    
