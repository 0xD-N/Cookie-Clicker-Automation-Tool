from selenium.webdriver.opera.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from Automation.Automation import Automation
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

def getElement(driver: WebDriver, xPath, multiple=False, wait=10) -> WebElement:
    try:
        if(multiple):
            code: WebElement = (WebDriverWait(driver, wait).until(lambda d: d.find_elements(By.XPATH, xPath)))
            return code
        
        else:
            code: WebElement = (WebDriverWait(driver, wait).until(lambda d: d.find_element(By.XPATH, xPath)))
            return code
            
    except TimeoutException:
        
        driver.close()
        time.sleep(1)
        os.system("cls")
        print(f"\nCouldn't find the speficied path: {xPath}")
        driver.quit()
        
    except Exception as e:
        
        driver.close()
        time.sleep(1)
        os.system("cls")
        print(f"\nAN ERROR HAS OCCURED")
        print(f"\nLine {e.__traceback__.tb_lineno}: {e}")
        driver.quit()

def start(clicksPerSecond = 1):
    
    SITE = "https://orteil.dashnet.org/cookieclicker/"
    
    A = Automation().getDriver()
    
    try:
        
        A.get(SITE)
        
        cookie = getElement(A, "(//*[@id=\"bigCookie\"])")
        
        output = getElement(A, "//*[@id=\"cookies\"]")
        
        cookie_amount = int(output.text[:output.text.index(" ")])
        
        products = getElement(A, "//*//span[contains(@id, \"productPrice\") and @class=\"price\"]//ancestor::div[contains(@class, \"product\")]", True)
        
        while(cookie_amount < 100000):
            
            for i in range(clicksPerSecond):
                cookie.click()
            
            cookie_amount = int(output.text[:output.text.index(" ")].replace("\n", "").replace(",", ""))
            
            for i in range(len(products)-1, -1, -1):
               
                if("unlocked" in products[i].get_attribute("class")):
                    content_div = products[i].find_element(By.CLASS_NAME, "content")
                    
                    price = int(content_div.find_element(By.CLASS_NAME, "price").text.replace(",", "").split("\n")[0])
                    
                    if(cookie_amount >= price):
                        products[i].click()
                    
            
        os.system("cls")
        A.quit()
        
    #Functional. Don't touch this
    except Exception as e:
        
        A.quit()
        time.sleep(1)
        os.system("cls")
        print(f"\nAN ERROR HAS OCCURED")
        print(f"\nLine {e.__traceback__.tb_lineno}: {e}")
    
# //*//span[contains(@id, "productPrice") and @class="price"]//ancestor::div[contains(@class, "product")]     
    
if __name__ == "__main__":
    start(2)
    


#in the div with dash-center class, it's contents are empty until the countdown of the game begins
#then we wait 3 seconds before typing again
#class="dash-letter is-correct is-typed"
#class="dash-letter is-waiting"