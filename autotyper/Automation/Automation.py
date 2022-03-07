from selenium import webdriver
from selenium.webdriver.opera.options import Options

#Selenium Driver. If you want to use chrome (or any browser): 

# download the chrome binary for your specific chrome version
# Move it to a path that is less likely to have issues (preferably in C:\Program Files (x86))
# change import above to (from selenium.webdriver.chrome.options)

#and lastly change the binary path in Automation class

class Automation():
    
    __BINARY_PATH = r"C:\Program Files (x86)\operaDriver\operadriver.exe"
    
    def __init__(self):
        
        self.__options = Options()
        
        self.__options.add_argument(r"--user-data-dir=C:\Users\david\AppData\Roaming\Opera Software\Opera Stable")
        self.__options.add_argument('--disable-blink-features=AutomationControlled')
        self.__options.add_argument('--ignore-certificate-errors')
        self.__options.add_argument('--headless')
        self.__options.add_argument('--profile-directory=Default') 
        self.__options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.__options.add_experimental_option('useAutomationExtension', False)
        self.__options.add_experimental_option("w3c", True)

        self.__driver = webdriver.Opera(executable_path=self.__BINARY_PATH, options=self.__options)
    
    def getDriver(self):
        return self.__driver