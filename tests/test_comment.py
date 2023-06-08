from datetime import datetime
from pageobjects.common_objects import common_objects
from src.testproject.decorator import report
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time
from pageobjects.comment_page import CommentPage
import sys
from tests.test_base import BaseTestCase
import re
import os

class Test_Comment(BaseTestCase):

    def tearDown(self):
        self.driver.delete_all_cookies()


    @report(test='Comment Display Test')
    def test_comment_display(self):
        self.driver.find_element_by_id("Project").click()
        if 'projectList' not in self.driver.current_url:
            self.driver.find_element_by_xpath('//*[@class="group"]//*[contains(text(),"← 프로젝트 리스트")]').click()        

        try:
            project_list = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="divTable"]//*[@class="subject"]')))
            project_list[0].click()
            
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="comment"]//*[contains(text(),"댓글 작성")]'))).click()
            comment_page = CommentPage()
            comment_page.find_comment_edit_objects(self.driver)
            comment_page.validate_comment_input_is_present()
            comment_page.validate_comment_upload_file_is_present()
            comment_page.validate_comment_cancel_is_present()
            comment_page.validate_comment_add_is_present()
                    
        except Exception as e:
            self.driver.report().step(description='Comment display Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)

    @report(test='Comment Add Test')
    def test_comment_add(self):
        try:
            comment_page = CommentPage()
            comment_page.find_comment_edit_objects(self.driver)
            now = datetime.now()
            comment_str = 'Automation Comment Add ' + now.strftime('%m%d%H%M%S')
            comment_page.comment_input.send_keys(comment_str)
            comment_page.comment_add.click()

            # 추가된 댓글 확인
            comment_xpath = '//*[@class="comment"]//*[contains(text(), "' + comment_str + '")]'
            time.sleep(1)
            comment_page.find_comment_info(self.driver, comment_xpath)
            
            self.assertEqual(self.driver.find_element_by_class_name('name').text, comment_page.user_name, '로그인한 사용자 이름과 댓글 작성자 불일치')
            self.assertEqual(now.strftime("'%y.%m.%d. %H:%M"), comment_page.comment_time, '시간 불일치')
            self.assertEqual(comment_str, comment_page.comment_content.text, '댓글 내용 불일치')
            
        except Exception as e:
            self.driver.report().step(description='Comment add Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)

    @report(test='Comment Modify Test')
    def test_comment_modify(self):
        try:
            comment_list = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="edit"]//*[contains(text(),"수정")]')))
            comment_list[0].click()
            
            comment_page = CommentPage()
            comment_page.find_comment_edit_objects(self.driver)
            comment_page.comment_input.send_keys("수정")
            # 파일 첨부
            file = self.driver.find_element_by_xpath("//*[@class='edit-cont']//input[@type='file']")
            file_name = 'kakaofreinds.png'
            abspath_testfile = os.path.abspath("utils/" + file_name)
            file.send_keys(abspath_testfile)
            # file.send_keys("C:\\Users\\USER\\Pictures\\" + file_name)

            comment_page.comment_add.click()
            time.sleep(3)
            # 수정된 댓글 확인
            comment_xpath = '//*[@class="text-comment"]//*[contains(text(), "수정")]'
            
            comment_page.find_comment_info(self.driver, comment_xpath)
            
            self.assertIn("수정", comment_page.comment_content.text, '댓글 내용 불일치')            
            self.assertIn("수정됨", comment_page.comment_info.text, '수정됨 표시 누락')
            self.assertIn(file_name, comment_page.comment_info.find_element_by_class_name('comment-file').text, '첨부파일 불일치')
            
            self.driver.execute_script("arguments[0].setAttribute('contenteditable','false')", comment_page.comment_input)

        except Exception as e:
            self.driver.report().step(description='Comment Modify Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)        


    @report(test='Comment Delete Test')
    def test_comment_delete(self):
        try:
            comment_page = CommentPage()
            comment_count = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="comment"]//*[contains(text(),"댓글 작성")]'))).text
            count = int(re.search('\(([^)]+)', comment_count).group(1))
            # 수정된 댓글을 삭제
            comment_xpath = '//*[@class="text-comment"]//*[contains(text(), "수정")]'
            comment_page.find_comment_info(self.driver, comment_xpath)
            time.sleep(1)
            comment_page.delete_btn.click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="app"]//*[contains(text(),"확인")]').click()
            time.sleep(1)
            # 삭제 됐는지 확인
            comment_count = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="comment"]//*[contains(text(),"댓글 작성")]'))).text
            if '(' in comment_count:
                after_count = int(re.search('\(([^)]+)', comment_count).group(1)) 
            else:
                after_count = 0
            
            self.assertEqual(count-1, after_count, '삭제 후 댓글 수 불일치')          
            
        except Exception as e:
            self.driver.report().step(description='Comment Delete Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)     

    @report(test='Reply Add Test')
    def test_reply_add(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="comment"]//*[contains(text(),"답글작성")]'))).click()
            
            comment_page = CommentPage()
            comment_page.find_comment_edit_objects(self.driver)
            now = datetime.now()
            reply_str = 'Automation Reply Add ' + now.strftime('%m%d%H%M%S')
            comment_page.comment_input.send_keys(reply_str)
            comment_page.comment_add.click()

            # 추가된 댓글 확인
            reply_xpath = '//*[@class="comment"]//*[contains(text(), "' + reply_str + '")]'
            time.sleep(1)
            comment_page.find_comment_info(self.driver, reply_xpath)
            
            self.assertEqual(self.driver.find_element_by_class_name('name').text, comment_page.user_name, '로그인한 사용자 이름과 댓글 작성자 불일치')
            self.assertEqual(now.strftime("'%y.%m.%d. %H:%M"), comment_page.comment_time, '시간 불일치')
            self.assertEqual(reply_str, comment_page.comment_content.text, '댓글 내용 불일치')
            
        except Exception as e:
            self.driver.report().step(description='Reply add Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)            

    @report(test='Reply Modify Test')
    def test_reply_modify(self):
        try:
            comment_list = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="comment-sub-box"]//*[contains(text(),"수정")]')))
            comment_list[0].click()
            
            comment_page = CommentPage()
            comment_page.find_comment_edit_objects(self.driver)
            comment_page.comment_input.send_keys("수정")

            comment_page.comment_add.click()
            time.sleep(3)
            # 수정된 댓글 확인
            comment_xpath = '//*[@class="text-comment"]//*[contains(text(), "수정")]'
            
            comment_page.find_comment_info(self.driver, comment_xpath)
            
            self.assertIn("수정", comment_page.comment_content.text, '댓글 내용 불일치')            
            self.assertIn("수정됨", comment_page.comment_info.text, '수정됨 표시 누락')
            
        except Exception as e:
            self.driver.report().step(description='Reply Modify Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)        

    @report(test='Reply Delete Test')
    def test_reply_delete(self):
        try:
            comment_page = CommentPage()
            
            # 수정된 댓글을 삭제
            comment_xpath = '//*[@class="comment-sub-box"]//*[@class="text-comment"]//*[contains(text(), "수정")]'
            comment_page.find_comment_info(self.driver, comment_xpath)
            reply_content = comment_page.comment_content.text
            reply_count = len(self.driver.find_elements_by_class_name('comment-list-view'))
            time.sleep(1)
            comment_page.delete_btn.click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="app"]//*[contains(text(),"확인")]').click()
            time.sleep(1)
            # 삭제 됐는지 확인
            all_list = self.driver.find_elements_by_class_name('comment-list-view')
            
            for content in all_list:
                self.assertNotIn(reply_content, content.text, '삭제된 답글과 일치하는 글 존재함')
            self.assertEqual(reply_count-1, len(all_list), '삭제 후 댓글 수 불일치')    

            
        except Exception as e:
            self.driver.report().step(description='Reply Delete Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)  