import unittest
import time
import sys

from src.testproject.decorator import report
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from pageobjects.admin_page import admin_page
from values import db_data
from values import strings
from webdriver import Driver
from tests.test_base import BaseTestCase

class Test_Local_admin(BaseTestCase):
    
    common = None


    def setUp(self):
        self.driver.get(strings.base_url)
   

    def tearDown(self):
        self.driver.delete_all_cookies()
        # self.driver.close()
        # self.driver.quit()

    # @classmethod
    # def tearDownClass(cls):
    #     cls.driver.quit()
    
    @report(test='Admin Corp List Check')
    def test_corpListCheck(self):
        
        #로그인
        self.driver.find_element_by_xpath('//*[@id="login"]/div/div/div/div/button').click()
        time.sleep(2)
        #어드민 메뉴 클릭
        self.driver.find_elements_by_class_name('global-nav')[3].click()
        time.sleep(2)
        #어드민 화면 elements
        adminPage = admin_page.admin_page(self.driver)
        #회원사 관리 메뉴 클릭
        adminPage.corpBtn.click()
        #self.driver.find_elements_by_class_name('admin-btn')[2].click()

        time.sleep(2)
        #테이블 전체보기
        self.driver.find_element_by_xpath('//*[@id="admin-corp"]/div[3]/div/div[2]/div[2]/label/div').click()
        self.driver.find_element_by_xpath('//*[@id="qvs_2"]/div[8]/div[2]/div').click()

        #회원사 리스트 테이블
        table = self.driver.find_element_by_id('qvs_1')
        tr_list = table.find_elements_by_tag_name('tr')
        
        corp_weblist = []
        for tr in tr_list:
            td_list = tr.find_elements_by_tag_name('td')
            
            temp = {
                'corp_nm': td_list[1].text, 
                'rpsv_nm': td_list[2].text,
                'upjong_nm': td_list[3].text,
                'etsr_no': td_list[4].text,
                'chrg_clerk_nm': td_list[5].text,
                'chrg_clerk_tel_no': td_list[6].text,
                'memo_txt': td_list[7].text,
                'cotr_start_dy': td_list[8].text,
                'cotr_end_dy': td_list[9].text,
                'reg_dy': td_list[10].text,
                'upd_dy': td_list[11].text
            }  
            
            corp_weblist.append(temp)
            
        corp_db = db_data.db_data().fetch_data(strings.corp_sql)
        
        for corp_web_dict in corp_weblist:
            for corp_db_dict in corp_db:
                if(corp_web_dict == corp_db_dict):
                    corp_web_dict['result'] = True
                    break

        
        for corp_dict in corp_weblist:
            if (corp_dict.get('result') == None):
                corp_dict['result'] = False

        for corp_temp in corp_weblist:
            print(corp_temp)
            print('\n')

    @report(test='Admin Msg List Check')
    def test_msgListCheck(self):
        
        #로그인
        self.driver.find_element_by_xpath('//*[@id="login"]/div/div/div/div/button').click()
        time.sleep(2)
        #어드민 메뉴 클릭
        self.driver.find_elements_by_class_name('global-nav')[3].click()
        time.sleep(2)
        #어드민 화면 elements
        adminpage = admin_page.admin_page(self.driver)

        #메세지 관리 메뉴 클릭
        adminpage.msgBtn.click()
        #self.driver.find_elements_by_class_name('admin-btn')[0].click()

        time.sleep(2)
        
        #메시지 리스트 테이블
        table = self.driver.find_element_by_class_name('q-table')
        tbody = table.find_element_by_class_name('q-virtual-scroll__content')
        tr_list = tbody.find_elements_by_tag_name('tr')
        
        msg_weblist = []
        for tr in tr_list:
            td_list = tr.find_elements_by_tag_name('td')
            
            temp = {
                'msg_job_cd': td_list[1].text,
                'msg_cd': td_list[2].text,
                'msg_txt': td_list[3].text,
                'msg_type_cd': td_list[4].text,
                'reg_dy': td_list[5].text
            }  
            
            msg_weblist.append(temp)
            
        msg_db = db_data.db_data().fetch_data(strings.msg_sql)
        
        for msg_web_dict in msg_weblist:
            for msg_db_dict in msg_db:
                if(msg_web_dict == msg_db_dict):
                    msg_web_dict['result'] = True
                    break

        
        for msg_dict in msg_weblist:
            if (msg_dict.get('result') == None):
                msg_dict['result'] = False

        for msg_temp in msg_weblist:
            print(msg_temp)
            print('\n')                    
            
            
if __name__ == "__main__":
    unittest.main()
        
    