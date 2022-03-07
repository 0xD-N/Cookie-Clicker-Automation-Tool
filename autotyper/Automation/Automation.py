from selenium import webdriver
from selenium.webdriver.opera.options import Options

class Automation():
    
    BINARY_PATH = r"C:\Program Files (x86)\operaDriver\operadriver.exe"
    
    def __init__(self):
        
        options = Options()
        
        options.add_argument(r"--user-data-dir=C:\Users\david\AppData\Roaming\Opera Software\Opera Stable")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless')
        options.add_argument('--profile-directory=Default') 
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("w3c", True)

        self.driver = webdriver.Opera(executable_path=self.BINARY_PATH, options=options)
    
    def getDriver(self):
        return self.driver