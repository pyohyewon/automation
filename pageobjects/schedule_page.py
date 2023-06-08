from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SchedulePage:
    
    def __init__(self, driver):
        self.driver = driver
        try:
            self.sortList = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"정렬 선택")]')))
            self.projectFilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"프로젝트 전체 보기")]')))
            self.tagFilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@role="button"]//*[contains(text(),"태그 전체 보기")]')))
            self.calendar = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'calender-range')))
            self.statusFilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="schd-title"]//*[contains(text(),"완료ㆍ보류 표시")]')))
            self.bookmarkFilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="schd-title"]//*[contains(text(),"북마크 필터")]')))
            self.zoomin = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="schd-tab"]//*[contains(text(),"add")]')))
            self.zoomout = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="schd-tab"]//*[contains(text(),"remove")]')))
            self.dayFilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="schd-tab"]//*[contains(text(),"일")]')))
            self.weekFilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="schd-tab"]//*[contains(text(),"주")]')))
            self.monthFilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="schd-tab"]//*[contains(text(),"월")]')))
            self.quarterFilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="schd-tab"]//*[contains(text(),"분기")]')))
            self.foldUnfoldBtn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'gantt-open-close')))
            self.projCreate = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="gantt_grid"]//*[contains(text(),"프로젝트 생성")]')))
            self.gridFoldBtn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'gridFoldingButton')))
            time.sleep(3)
            self.ganttList = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'gantt_row')))
            time.sleep(3)
            self.ganttBars = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'gantt_bar_task')))
        except Exception as e:
            self.driver.report().step(description='SchedulePage element exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)
        
        
    def find_ganttList(self):
        self.ganttList = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'gantt_row')))
        return self.ganttList        
    
    def validate_ganttList_is_present(self):    
        for row in self.ganttList: 
            # print(str(row.is_displayed()))
            assert row.is_enabled()
        

    def validate_ganttBars_is_present(self):
        for bar in self.ganttBars:
            assert bar.is_enabled()
        
    def validate_sortList_is_present(self):
        assert self.sortList.is_displayed()

    def validate_projectFilter_is_present(self):
        assert self.projectFilter.is_displayed()
    
    def validate_tagFilter_is_present(self):
        assert self.tagFilter.is_displayed()        
    
    def validate_calendar_is_present(self):
        assert self.calendar.is_displayed()

    def validate_statusFilter_is_present(self):
        assert self.statusFilter.is_displayed()    

    def validate_bookmarkFilter_is_present(self):
        assert self.bookmarkFilter.is_displayed()      

    def validate_zoomin_is_present(self):
        assert self.zoomin.is_displayed()      

    def validate_zoomout_is_present(self):
        assert self.zoomout.is_displayed()      

    def validate_dayFilter_is_present(self):
        assert self.dayFilter.is_displayed()      

    def validate_weekFilter_is_present(self):
        assert self.weekFilter.is_displayed()      

    def validate_monthFilter_is_present(self):
        assert self.monthFilter.is_displayed()      

    def validate_quarterFilter_is_present(self):
        assert self.quarterFilter.is_displayed()     

    def validate_foldUnfoldBtn_is_present(self):
        self.foldUnfoldBtn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'gantt-open-close')))
        assert self.foldUnfoldBtn.is_displayed()    
        return self.foldUnfoldBtn 

    def validate_projCreate_is_present(self):
        assert self.projCreate.is_displayed()     

    def validate_gridFoldBtn_is_present(self):
        self.gridFoldBtn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'gridFoldingButton')))
        assert self.gridFoldBtn.is_displayed()    
        return self.gridFoldBtn