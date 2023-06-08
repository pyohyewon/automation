from src.testproject.sdk.drivers import webdriver

class Driver:
    strToken = 'AOuPitTzWxH8SEyuwHr-Uxb8T-YfGBQIfylCpycIXiA1'
        
    def __init__(self, testjobname):
        self.instance = webdriver.Chrome(token=self.strToken, projectname='Teamply Project', jobname=testjobname)

    def navigate(self, url):
        if isinstance(url, str):
            self.instance.get(url)
        else:
            raise TypeError("URL must be a string.")