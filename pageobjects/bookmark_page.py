from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookmarkPage:

    def __init__(self, driver):
        self.driver = driver
        try: # 북마크 타이틀바
            self.bookmark_title = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))
            self.bookmark_exit = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="projlist-title"]//*[contains(text(),"exit_to_app")]'))) #나가기
            self.bookmark_compfilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="projlist-title"]//*[contains(text(),"완료·보류 표시")]')))
            self.bookmark_permfilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="projlist-title"]//*[contains(text(),"전체 권한")]')))
            self.bookmark_statusfilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="projlist-title"]//*[contains(text(),"전체 상태")]')))
            self.bookmark_table = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'divTable')))
            self.bookmark_tableheader = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'divTable-header')))

            # Locators
            self.bookmark_columnheaders = '//*[contains(@class,"divTable-head")][contains(@class,"m-pointer")]'
            self.bookmark_filterlist = '//ul[@class="list"]/li'
            self.bookmark_list = 'divTable-body'
            self.bookmark_nodata = 'no-data-style0'
        except Exception as e:
            self.driver.report().step(description='Bookmark page element exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)

    def validate_bookmark_title_is_present(self):
        assert self.bookmark_title.is_displayed()

    def validate_bookmark_exit_is_present(self):
        assert self.bookmark_exit.is_displayed()

    def validate_bookmark_compfilter_is_present(self):
        assert self.bookmark_compfilter.is_displayed()
      
    def validate_bookmark_permfilter_is_present(self):
        assert self.bookmark_permfilter.is_displayed()
      
    def validate_bookmark_statusfilter_is_present(self):
       assert self.bookmark_statusfilter.is_displayed()

    def validate_bookmark_table_is_present(self):
       assert self.bookmark_table.is_displayed()

    def validate_bookmark_tableheader_is_present(self):
        assert self.bookmark_tableheader.is_displayed()
  

