import unittest
import time

from webdriver import Driver
from utils.load_json import LoadJson
from pageobjects.login_page import login_page


class BaseTestCase(unittest.TestCase):
  
	driver = Driver("Teamply Program Sanity Test").instance

	base_url = LoadJson.json_env_data[3].get('base_url')
	user_data = LoadJson.json_user_data[0]
	user_email = user_data.get('email')
	password = user_data.get('password')
 
	def login(self):	  
		self.driver.get(self.base_url)

		self.assertEqual(self.driver.current_url.split('/')[-1], 'login', "The page is not on the login")
		time.sleep(1)
		try:
			loginScreen = login_page(self.driver)
			loginScreen.emailField.send_keys(self.user_email)
			loginScreen.pwField.send_keys(self.password)
			
			loginScreen.loginBtn.click()
			time.sleep(1)
			
		except Exception as e:
			self.driver.report().step(description='Login Exception', message='Occurred Exception'+str(e), passed=False, screenshot=True)

	def driver_quit(self):
		self.driver.delete_all_cookies()
		self.driver.quit()
		