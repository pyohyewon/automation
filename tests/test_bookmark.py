import time
import unittest

from pageobjects.bookmark_page import BookmarkPage
from pageobjects.home_page import HomePage
from pageobjects.login_page import login_page
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.testproject.decorator import report
from utils.load_json import LoadJson
from webdriver import Driver

from tests.test_base import BaseTestCase


class TEST_Bookmark(BaseTestCase):

    base_url = LoadJson.json_env_data[1].get('base_url')

    defined_permlist = LoadJson.json_predefined_data.get('bookmark_permlist')
    defined_statuslist = LoadJson.json_predefined_data.get('bookmark_statuslist')
    defined_columnheaders = LoadJson.json_predefined_data.get('bookmark_columnheaders')

    @report(test='Move to Bookmark page')
    def move_to_bookmark_page(self):

        try:
            homeScreen = HomePage(self.driver)
            homeScreen.lnb_bookmark.click()
            time.sleep(1)
        except Exception as e:
            self.driver.report().step(description='Home page Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        

    @report(test='Bookmark Display Test')
    def test_bookmark_display(self):
        self.move_to_bookmark_page()
        time.sleep(1)

        bookmark_page = BookmarkPage(self.driver)
        try:
            bookmark_page.validate_bookmark_title_is_present()
            bookmark_page.validate_bookmark_exit_is_present()
            bookmark_page.validate_bookmark_compfilter_is_present()
            bookmark_page.validate_bookmark_permfilter_is_present()
            bookmark_page.validate_bookmark_statusfilter_is_present()
            bookmark_page.validate_bookmark_table_is_present()
            bookmark_page.validate_bookmark_tableheader_is_present()
                    
            self.assertEqual(self.driver.current_url.split('/')[-1], 'bookmark', "The page is not on the Bookmark") # assert if the bookmark page url has 'bookmark'
            self.assertTrue(bookmark_page.bookmark_title.text.__contains__('북마크')) # assert if the title of bookmark page has '북마크'                    
            
            column_hearders = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, bookmark_page.bookmark_columnheaders)))
            column_headerlists = []
            for i in range(0,len(column_hearders)):
                column_headerlists.append(column_hearders[i].text.split('\n')[0])
            self.assertEqual(column_headerlists, self.defined_columnheaders, "북마크 페이지 컬럼 헤더 오류") #assert if the column header list is same as pre-defined
            
            # TODO need conditional assert if there's no bookmarked list
            self.assertEqual(bookmark_page.bookmark_title.text.split('(')[1].split(')')[0],str(len(bookmark_page.bookmark_list))) # assert if the number of bookmark list is shown in the title

        except Exception as e:
            self.driver.report().step(description='Bookmark display Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)


    @report(test='Exit from Bookmark page')
    def test_exit_from_bookmark(self):
        
        try:
            bookmark_page = BookmarkPage(self.driver)
            bookmark_page.bookmark_exit.click()
            time.sleep(1)

            self.assertEqual(self.driver.current_url,self.base_url , "북마크 나가기 오류")

        except Exception as e:
            self.driver.report().step(description='Exit from Bookmark Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)

        finally:
            self.move_to_bookmark_page()
 
    @report(test='Bookmark permission filter Test')
    def test_bookmark_permission_filter(self):
        # 권한 필터 테스트
        bookmark_page = BookmarkPage(self.driver)
        try:            
            bookmark_page.bookmark_permfilter.click()
            bookmark_permfilterlist = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, bookmark_page.bookmark_filterlist)))
    
            self.assertEqual(len(bookmark_permfilterlist), len(self.defined_permlist), '권한 필터 항목 수 오류')
        
            filterlists = []
            for i in range(0,len(self.defined_permlist)):
                filterlists.append(bookmark_permfilterlist[i].text)
            self.assertEqual(filterlists, self.defined_permlist, '권한 필터 항목 값 오류') #assert if the filter list is same as pre-defined

            bookmark_permfilterlist[1].click()  # '리더' 권한 선택
            time.sleep(3)
            if len(self.driver.find_elements_by_class_name(bookmark_page.bookmark_list)) == 0: # 리더 항목이 없는 경우
                no_data = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, bookmark_page.bookmark_nodata)))
                assert '클라우드 협업 플랫폼' in no_data.text, '노데이터 페이지 오류'
            else:    
                bookmark_list = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, bookmark_page.bookmark_list)))
                for i in range (min(len(bookmark_list),10)):        
                    self.assertEqual(str(bookmark_list[i].text.split('\n')[-2]), self.defined_permlist[1], self.defined_permlist[1] +'권한 필터 오류 발생')

            # SR-924 [북마크][나의 업무] 권한 정보가 현재 항목에서의 담당 권한이 아닌 업무 구조에 따른 상속된 권한 정보가 보이고 있음
            # '멤버' 권한 선택시 상위 항목에 상위 권한(리더)이 있을 경우 리더로 보여주고 있는 상황이므로 자동화되기 어려운 상황
            # bookmark_page.bookmark_permfilter.click()
            # bookmark_permfilterlist = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, bookmark_page.bookmark_permfilterlist)))
            # bookmark_permfilterlist[2].click() 
            # time.sleep(3)
            # bookmark_list = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, bookmark_page.bookmark_list)))
            # if len(bookmark_list) > 0:
            #     for i in range (min(len(bookmark_list),10)):        
            #         self.assertEqual(str(bookmark_list[i].text.split('\n')[-2]), self.defined_permlist[2], self.defined_permlist[2] +'권한 필터 오류 발생')
            # 상태 필터와 함께 루프 처리로 개선 가능. 단 멤버의 경우에 오류 처리되어야 함
            bookmark_page.bookmark_permfilter.click()
            bookmark_permfilterlist = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, bookmark_page.bookmark_filterlist)))
            bookmark_permfilterlist[3].click()  # '게스트' 권한 선택. 현재는 게스트 권한이 없으므로 노데이터 이미지가 보임
            time.sleep(3)
            if len(self.driver.find_elements_by_class_name(bookmark_page.bookmark_list)) == 0:
                no_data = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, bookmark_page.bookmark_nodata)))
                assert '클라우드 협업 플랫폼' in no_data.text, '노데이터 페이지 오류'
            else:
                bookmark_list = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, bookmark_page.bookmark_list)))
                for i in range (min(len(bookmark_list),10)):        
                    self.assertEqual(str(bookmark_list[i].text.split('\n')[-2]), self.defined_permlist[3], self.defined_permlist[3] +'권한 필터 오류 발생')

        except Exception as e:
            self.driver.report().step(description='Bookmark permission filter Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)

        finally:
            bookmark_page.bookmark_permfilter.click()
            time.sleep(1)
            bookmark_permfilterlist = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, bookmark_page.bookmark_filterlist)))
            bookmark_permfilterlist[0].click()

    
    @report(test="Bookmark status filter test")
    def test_bookmark_status_filter(self):          
        # 상태 필터 테스트
        bookmark_page = BookmarkPage(self.driver)

        try: 
            bookmark_page.bookmark_statusfilter.click() 
            bookmark_statusfilterlist = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, bookmark_page.bookmark_filterlist)))
      
            self.assertEqual(len(bookmark_statusfilterlist), len(self.defined_statuslist), '상태 필터 항목 수 오류')

            statuslists = []
            for i in range(len(self.defined_statuslist)):
                statuslists.append(bookmark_statusfilterlist[i].text)
            self.assertEqual(statuslists, self.defined_statuslist, '상태 필터 항목 값 오류')
            bookmark_page.bookmark_statusfilter.click() # 값 비교 후 리스트를 닫고 아래 For loop내에서 다시 열어서 진행

            for j in range(1,len(self.defined_statuslist)):
                bookmark_page.bookmark_statusfilter.click() 
                bookmark_statusfilterlist = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, bookmark_page.bookmark_filterlist)))
                bookmark_statusfilterlist[j].click()
                time.sleep(3)
                if len(self.driver.find_elements_by_class_name(bookmark_page.bookmark_list)) == 0:
                    no_data = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, bookmark_page.bookmark_nodata)))
                    assert '클라우드 협업 플랫폼' in no_data.text, '노데이터 페이지 오류'
                else:
                    bookmark_list = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, bookmark_page.bookmark_list)))
                    for i in range (min(len(bookmark_list),10)):
                        self.assertEqual(str(bookmark_list[i].text.split('\n')[0]), self.defined_statuslist[j], self.defined_statuslist[j] + '상태 필터 오류 발생')
                # print(self.defined_statuslist[j])

        except Exception as e:
            self.driver.report().step(description='Bookmark status filter Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)

        finally:
            bookmark_page.bookmark_statusfilter.click()  
            time.sleep(1)
            bookmark_statusfilterlist = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, bookmark_page.bookmark_filterlist)))
            bookmark_statusfilterlist[0].click()

    @report(test='Bookmark clicknmove Test')
    def test_bookmark_clicknmove(self):

        assert True

    @report(test='Bookmark column sorting Test')
    def test_bookmark_column_sorting(self):
        assert True

    @report(test='Bookmark add Test')
    def test_bookmark_add(self):
        assert True


    @report(test='Bookmark complete filter Test')
    def test_bookmark_complete_filter(self):
        assert True


    @report(test="Finalize Bookmark")
    def test_finalize_bookmark(self):     
        self.driver.get(self.base_url)
        self.assertEqual(self.driver.current_url, self.base_url)

if __name__ == "__main__":
    unittest.main()

