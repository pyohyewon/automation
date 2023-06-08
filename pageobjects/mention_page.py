from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver import Driver

class MentionPage:

    def __init__(self, driver):
        self.driver = driver
        try: # 멘션 타이틀바
            self.mention_title = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))
            self.mention_exit = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="projlist-title"]//*[contains(text(),"exit_to_app")]'))) #나가기
            self.mention_viewall = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"전체보기")]')))
            self.mention_comment = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"댓글")]')))
            self.mention_chat = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="projlist"]//*[contains(text(),"채팅")]')))
            self.mention_doc = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"문서")]')))
            self.mention_report = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"리포트")]')))
            self.mention_filterlist = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@role="button"]//*[@class="txt"]')))
            # 멘션 리스트에 멘션 없을수도 있기 때문에 find_elements 함수 사용
            self.mention_list = self.driver.find_elements_by_class_name('tbstyle')
            self.mention_path = self.driver.find_elements_by_xpath('//*[@class="mention-arr"]//*[contains(text(),"멘션")]')
        except Exception as e:
            self.driver.report().step(description='Mention page element exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)

    def validate_mention_title_is_present(self):
        assert self.mention_title.is_displayed()

    def validate_mention_exit_is_present(self):
        assert self.mention_exit.is_displayed()

    def validate_mention_viewall_is_present(self):
        assert self.mention_viewall.is_displayed()
      
    def validate_mention_comment_is_present(self):
        assert self.mention_comment.is_displayed()
      
    def validate_mention_chat_is_present(self):
        assert self.mention_chat.is_displayed()

    def validate_mention_doc_is_present(self):
        assert self.mention_doc.is_displayed()

    def validate_mention_report_is_present(self):
        assert self.mention_report.is_displayed()
  

