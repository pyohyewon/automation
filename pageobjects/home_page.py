from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:

    def __init__(self, driver):
        self.driver = driver
        # gnb elements
        self.gnb = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'gnb')))
        self.gnb_menu = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="gnb"]//*[@role="button"]')))
        self.gnb_logo = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="gnb"]//*[contains(text(),"로고")]')))

        self.gnb_home = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'Home')))
        self.gnb_project = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'Project')))
        self.gnb_schedule = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'Schedule')))
        self.gnb_report = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'Report')))

        # lnb elements
        self.lnb = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'lnb')))
        self.lnb_menu = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="lnb"]//*[@role="button"]'))) #lnb_menu returns multiple web elements in lnb
        self.lnb_bookmark = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="lnb"]//*[contains(text(),"북마크")]'))) 
        self.lnb_myworks = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="lnb"]//*[contains(text(),"나의 업무")]')))
        self.lnb_mentions = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="lnb"]//*[contains(text(),"멘션")]')))
        self.lnb_filebox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="lnb"]//*[contains(text(),"파일 보관함")]')))
        self.lnb_network = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="lnb"]//*[contains(text(),"네트워크")]')))

        # home all elements
        self.my_project = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@class="home appContent"]//*[contains(text(),"나의 프로젝트")]')))
        self.banner = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="home appContent"]//*[@class="visual-img visual1"]')))
        # self.invited_project = 
        self.contact_admin = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="home appContent"]//*[contains(text(),"관리자 문의")]')))
        self.guide = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="home appContent"]//*[contains(text(),"이용자 가이드")]')))
        self.notice = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="home appContent"]//*[contains(text(),"공지사항")]')))
        self.customer_service = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="home appContent"]//*[contains(text(),"고객센터")]')))

    def validate_gnb_is_present(self):
        assert self.gnb.is_displayed()

    # def validate_gnb_menu_is_present(self):
    #     assert self.gnb_menu.is_displayed()

    def validate_gnb_logo_is_present(self):
        assert self.gnb_logo.is_displayed()


    def validate_gnb_home_is_present(self):
        assert self.gnb_home.is_displayed()

    def validate_gnb_project_is_present(self):
        assert self.gnb_project.is_displayed()

    def validate_gnb_schedule_is_present(self):
        assert self.gnb_schedule.is_displayed()

    def validate_gnb_report_is_present(self):
        assert self.gnb_report.is_displayed()


    def validate_lnb_is_present(self):
        assert self.lnb.is_displayed()

    # def validate_lnb_menu_is_present(self):
    #     assert self.lnb_menu.is_displayed()

    def validate_lnb_bookmark_is_present(self):
        assert self.lnb_bookmark.is_displayed()

    def validate_lnb_myworks_is_present(self):
        assert self.lnb_myworks.is_displayed()

    def validate_lnb_mentions_is_present(self):
       assert self.lnb_mentions.is_displayed()

    def validate_lnb_filebox_is_present(self):
        assert self.lnb_filebox.is_displayed()

    def validate_lnb_network_is_present(self):
       assert self.lnb_network.is_displayed()

    def validate_tab_title(self):
        assert 'Teamply' in self.driver.title

    def validate_home_elements(self):
        assert self.my_project.is_displayed()
        assert self.banner.is_displayed()
        assert self.contact_admin.is_displayed()
        assert self.guide.is_displayed()
        assert self.notice.is_displayed()
        assert self.customer_service.is_displayed()
      
