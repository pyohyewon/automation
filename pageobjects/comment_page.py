from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
class CommentPage:

    def find_comment_edit_objects(self, driver):
        self.driver = driver
        try: 
            self.comment_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]')))
            self.comment_cancel = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="comment"]//*[contains(text(),"취소")]')))
            self.comment_add = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="comment"]//*[contains(text(),"등록")]')))
            if 'reply' not in sys._getframe(1).f_code.co_name :
                self.comment_upload_file = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="comment"]//*[contains(text(),"attachment")]')))

            
        except Exception as e:
            self.driver.report().step(description='Comment element exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)

    def find_comment_info(self, driver, comment_xpath):
        self.driver = driver
        try: 
            self.comment_content = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, comment_xpath)))
            time.sleep(1)
            self.comment_info = self.comment_content.find_element_by_xpath('../../../../..//*[@class="comment-list-view"]')
            self.user_name = self.comment_info.find_element_by_class_name('comment-hdname').text
            self.comment_time = self.comment_info.find_element_by_xpath('.//span[contains(text(),"21.")]').text
            self.modify_btn = self.comment_info.find_element_by_xpath('.//span[contains(text(),"수정")]')
            self.delete_btn = self.comment_info.find_element_by_xpath('.//span[contains(text(),"삭제")]')
            if 'reply' not in sys._getframe(1).f_code.co_name :
                self.reply_btn = self.comment_info.find_element_by_xpath('.//span[contains(text(),"답글작성")]')

        except Exception as e:
            self.driver.report().step(description='Comment info element exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)            



    def validate_comment_input_is_present(self):
        assert self.comment_input.is_displayed()
    def validate_comment_upload_file_is_present(self):
        assert self.comment_upload_file.is_displayed()
    def validate_comment_cancel_is_present(self):
        assert self.comment_cancel.is_displayed()
    def validate_comment_add_is_present(self):
        assert self.comment_add.is_displayed()            


