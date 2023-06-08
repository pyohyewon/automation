from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class project_page:
    
    def find_main_objects(self, driver):
        self.driver = driver
        #self.createField = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "task-info-contents background-white")))
        self.title = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='제목을 입력하세요.']")))
        self.expectedEnd = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/main/div[2]/div/div/div[2]/div/div/div[4]/div[4]')))
        #self.calendar = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'q-date__calendar-item q-date__calendar-item--in')))
        #self.managementDep = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/main/div[2]/div/div/div[2]/div/div/div[5]/div[2]')))
        self.cancel = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"취소")]')))
        self.save = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"저장")]')))
        

    def find_main_modify_objects(self, driver):
        self.driver = driver
        self.title = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='제목을 입력하세요.']")))
        self.save = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"저장")]')))
        self.add_dept_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"playlist_add")]')))
        self.explain = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'explainTextArea')))
        self.tag = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Enter로 입력"]')))
        self.mst_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="마일스톤 내용을 입력하세요."]')))
        self.mst_date = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="날짜선택"]')))

    def find_sub_objects(self, driver):
        self.driver = driver
        self.title = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='제목을 입력하세요.']")))
        self.expectedEnd = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/main/div[2]/div/div[3]/div/div/div/div/div/div[4]/div[4]')))    
        self.save = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"저장")]')))
        self.explain = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'explainTextArea')))
        self.tag = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Enter로 입력"]')))
        self.pre_task = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@placeholder="이전 업무를 연결하세요."]')))
        self.next_task = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@placeholder="다음 업무를 연결하세요."]')))
        self.mst_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="마일스톤 내용을 입력하세요."]')))
        self.mst_date = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="날짜선택"]')))

    def find_task_objects(self, driver):
        self.driver = driver
        self.title = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='제목을 입력하세요.']")))
        self.expectedEnd = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/main/div[2]/div/div[3]/div/div/div/div/div/div[4]/div[4]')))    
        self.save = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"저장")]')))
        self.tag = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Enter로 입력"]')))
        self.pre_task = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@placeholder="이전 업무를 연결하세요."]')))
        self.next_task = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@placeholder="다음 업무를 연결하세요."]')))
        


    def validate_title_is_present(self):
        assert self.title.is_displayed()
    
    def validate_expectedEnd_is_present(self):
        assert self.expectedEnd.is_displayed()

    def validate_cancel_is_present(self):
        assert self.cancel.is_displayed()

    def validate_save_is_present(self):
        assert self.save.is_displayed()

    def validate_leader_name(self):
        self.profile_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="profile-info"]//*[@class="name"]'))).text
        self.leader_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="manager"]//*[@class="name  bgico-ti-check"]'))).text

        assert self.profile_name == self.leader_name

    
