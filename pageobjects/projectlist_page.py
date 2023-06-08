from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProjectlistPage:

    def __init__(self, driver):
        self.driver = driver
        # 프로젝트리스트 타이틀
        self.projectlist_title = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))
        self.projectlist_compfilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="projlist-title"]//*[contains(text(),"완료·보류 표시")]')))
        self.projectlist_nomemberfilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="projlist-title"]//*[contains(text(),"미소속 프로젝트 표시")]')))
        self.projectlist_periodfilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="projlist-title"]//span[contains(text(),"event")]')))
        self.projectlist_tagfilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="projlist-title"]//*[contains(text(),"태그 선택")]')))
        self.projectlist_projcreateButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="projlist-title"]//span[contains(text(),"프로젝트 생성")]')))
        try:
            self.projectlist_list = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="divTable-body"]')))
        except Exception as e:
            self.driver.report().step(description='projectlist page no data', message='Occurred Exception'+str(e), passed=False, screenshot=True)

    def validate_projectlist_title_is_present(self):
        assert self.projectlist_title.is_displayed()

    def validate_projectlist_compfilter_is_present(self):
        assert self.projectlist_compfilter.is_displayed()

    def validate_projectlist_nomemberfilter_is_present(self):
        assert self.projectlist_nomemberfilter.is_displayed()    

    def validate_projectlist_periodfilter_is_present(self):
       assert self.projectlist_periodfilter.is_displayed() 
      
    def validate_projectlist_tagfilter_is_present(self):
       assert self.projectlist_tagfilter.is_displayed()

    def validate_projectlist_projcreateButton_is_present(self):
       assert self.projectlist_projcreateButton.is_displayed()
    