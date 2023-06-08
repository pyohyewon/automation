import time
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.testproject.decorator import report
from pageobjects.mention_page import MentionPage
from webdriver import Driver
from tests.test_base import BaseTestCase
from utils.load_json import LoadJson


class TEST_Mention(BaseTestCase):

    defined_filterlist = LoadJson.json_predefined_data.get('mention_filterlist')
    current_url = ""
    def tearDown(self):
        self.driver.delete_all_cookies()

    @report(test='Move to Mention page')
    def move_to_mention_page(self):

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="lnb"]//*[contains(text(),"멘션")]'))).click()
            time.sleep(1)
        except Exception as e:
            self.driver.report().step(description='Home page Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        

    @report(test='Mention Display Test')
    def test_mention_display(self):
        self.current_url = self.driver.current_url
        self.move_to_mention_page()
        time.sleep(1)

        mention_page = MentionPage(self.driver)
        try:
            mention_page.validate_mention_title_is_present()
            mention_page.validate_mention_exit_is_present()
            mention_page.validate_mention_viewall_is_present()
            mention_page.validate_mention_comment_is_present()
            mention_page.validate_mention_chat_is_present()
            mention_page.validate_mention_doc_is_present()
            mention_page.validate_mention_report_is_present()
                    
            self.assertEqual(self.driver.current_url.split('/')[3], 'mentions', "The page is not on the mention") # assert if the mention page url has 'mention'
            self.assertTrue(mention_page.mention_title.text.__contains__('멘션')) # assert if the title of mention page has '멘션'                    
                        
            # TODO need conditional assert if there's no mentioned list
            self.assertEqual(mention_page.mention_title.text.split('(')[1].split(')')[0],str(len(mention_page.mention_list))) # assert if the number of mention list is shown in the title

        except Exception as e:
            self.driver.report().step(description='Mention display Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)


    @report(test='Exit from Mention page')
    def test_exit_from_mention(self):
        self.test_mention_display()
        try:
            mention_page = MentionPage(self.driver)
            mention_page.mention_exit.click()
            time.sleep(1)

            self.assertEqual(self.driver.current_url, self.current_url , "멘션 나가기 오류")

        except Exception as e:
            self.driver.report().step(description='Exit from Mention Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)

        finally:
            self.move_to_mention_page()
 

    @report(test='Mention viewall Test')
    def test_mention_viewall(self):
        # 전체보기 필터 테스트
        mention_page = MentionPage(self.driver)
        try:            
            mention_page.mention_viewall.click()
            # 멘션된 항목이 없을 경우 no-data 보이는지 확인
            if len(mention_page.mention_path) == 0:
                self.assertTrue(self.driver.find_element_by_class_name('no-data-style0').is_displayed(), "멘션된 항목 없지만 no-data 화면 제공되지 않음")
            # 멘션된 항목이 있을 경우 전체 개수 더한 후 타이틀에 표시되는 숫자와 비교
            else:
                mention_count = mention_page.mention_title.text.split('(')[1].split(')')[0]
                count_comment = 0
                count_chat = 0
                count_doc = 0
                count_report = 0
                for path in mention_page.mention_path:
                    if '댓글에' in path.text:
                        count_comment += 1
                    elif '채팅에' in path.text:
                        count_chat += 1
                    elif '문서에' in path.text:
                        count_doc += 1
                    elif '리포트에' in path.text:
                        count_report += 1
                    else: # 4가지 경우에 해당되지 않으면 error
                        raise Exception('댓글, 채팅, 문서, 리포트에 속하지 않음. 확인 필요.') 
                # 멘션된 항목이 있지만 count가 0이면 error
                self.assertNotEqual(count_report+count_chat+count_comment+count_doc, 0, '멘션된 항목 존재하지만 count가 0으로 집계됨. 확인 필요.')
                # 멘션된 전체 항목 개수와 타이틀에 표시되는 숫자 비교
                self.assertEqual(str(count_report+count_chat+count_comment+count_doc), mention_count, '전체 항목 개수와 타이틀에 표시된 숫자가 동일하지 않음')

        except Exception as e:
            self.driver.report().step(description='Mention view all Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)


    @report(test='Mention filter Test')
    def test_mention_filter(self):          
        # 댓글, 채팅, 문서, 리포트 필터 테스트
        mention_page = MentionPage(self.driver)

        try: 
            self.assertEqual(len(mention_page.mention_filterlist), len(self.defined_filterlist))

            filterlists = []
            for i in range(len(self.defined_filterlist)):
                filterlists.append(mention_page.mention_filterlist[i].text)
            self.assertEqual(filterlists, self.defined_filterlist)

            for i in range(1, len(mention_page.mention_filterlist)):
                mention_page.mention_filterlist[i].click()
                time.sleep(2)

                if filterlists[i] in ("채팅", "리포트"):
                    continue
                mention_page.mention_path = self.driver.find_elements_by_xpath('//*[@class="mention-arr"]//*[contains(text(),"멘션")]')
                for path in mention_page.mention_path:
                    self.assertIn(filterlists[i]+'에', path.text, '선택된 필터에 해당되지 않는 항목 존재하는 오류 발생' )

        except Exception as e:
            self.driver.report().step(description='Mention filter Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        finally:
            mention_page.mention_viewall.click()

    @report(test='Mention Card Test')
    def test_mention_card(self):
        # 멘션 카드 상세 정보 확인
        mention_page = MentionPage(self.driver)
        try: 
            time.sleep(2)
            for mention_item in mention_page.mention_list:
                # 시간 정보가 표시되는지 확인
                assert mention_item.find_element_by_class_name('ml10').is_displayed()
                # 아이콘이 표시되는지 확인
                assert mention_item.find_element_by_class_name('mention-icon').is_displayed()
                # 프로젝트 경로가 표시되는지 확인
                assert mention_item.find_element_by_xpath('//*[@class="mention-arr grey"]').is_displayed()
                # 멘션 내용이 표시되는지 확인
                assert mention_item.find_element_by_class_name('mention-txt').is_displayed()
                
            # 멘션 카드 클릭 시 해당 프로젝트로 이동하는지 확인
            path_element = mention_page.mention_list[0].find_element_by_css_selector("span[class*='dark']")
            path_name = path_element.text
            path_class = path_element.get_attribute("class")
            if 'bgico-ti-task-editor' in path_class:
                xpath_class = 'editor-title-view'
            elif 'bgico-ti-task' in path_class:
                xpath_class = 'bgico-sm-task'
            elif 'bgico-ti-sub' in path_class:
                xpath_class = 'bgico-sm-sub'
            elif 'bgico-ti-main' in path_class:
                xpath_class = 'bgico-sm-main'

            mention_page.mention_list[0].click()
            time.sleep(2)
            if xpath_class == 'editor-title-view':
                docs = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, xpath_class)))
                for doc in docs:
                    if path_name in doc.text:
                        equal_flag = True
                        break
                self.assertEqual(equal_flag, True, "멘션에 제공된 문서 이름 불일치 오류")
            else : 
                self.assertIn(path_name, WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, xpath_class))).text, "멘션에 제공된 업무(메인/하위/태스크) 이름 불일치 오류") 

        except Exception as e:
            self.driver.report().step(description='Mention Card Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)