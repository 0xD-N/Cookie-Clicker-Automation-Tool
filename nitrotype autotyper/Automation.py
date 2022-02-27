import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.opera.options import Options
from bs4 import BeautifulSoup
import time

class Automation():
    
    BINARY_PATH = r"C:\Program Files (x86)\operaDriver\operadriver.exe"
    
    def __init__(self):
        
        options = Options()
        options.add_experimental_option("w3c", True)
        options.add_argument(r"--user-data-dir=C:\Users\david\AppData\Roaming\Opera Software\Opera Stable")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Opera(executable_path=self.BINARY_PATH, options=options)
        
    def getSite(self, site):
        
        self.driver.get(site)
    
    def getElementByID(self, ID):
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, ID)))
        
        return self.driver.find_element(By.ID, ID)
    
    def getElementsByClass(self, CL):
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, CL)))
        
        return self.driver.find_elements(By.CLASS_NAME, CL)
    
    def exit(self):
        
        self.driver.quit()
        os.system("cls")