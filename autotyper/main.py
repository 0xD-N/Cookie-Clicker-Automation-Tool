from selenium.webdriver.opera.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from Automation.Automation import Automation
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

#gets element(s) in web page. Returns none if timeout reached
def getElement(driver: WebDriver, xPath, multiple=False, wait=10) -> WebElement | None:
    try:
        if(multiple):
            code: WebElement = (WebDriverWait(driver, wait).until(lambda d: d.find_elements(By.XPATH, xPath)))
            return code
        
        else:
            code: WebElement = (WebDriverWait(driver, wait).until(lambda d: d.find_element(By.XPATH, xPath)))
            return code
            
    except TimeoutException:
        
        time.sleep(1)
        os.system("cls")
        print(f"\nCouldn't find the speficied path: {xPath}")
        return None
        
    except StaleElementReferenceException as e:

        time.sleep(1)
        os.system("cls")
        print(f"\nAN ERROR HAS OCCURED")
        print(f"\nLine {e.__traceback__.tb_lineno}: {e}")
        
        return None

#gets cookies per second
def getCookiesPerSecond(element: WebElement) -> str:
    
    cookies_per_second = element.text.split("\n")
        
    if(len(cookies_per_second) == 3):
                cookies_per_second = cookies_per_second[2]
    else:
        cookies_per_second = cookies_per_second[1]
                    
    cookies_per_second = cookies_per_second[cookies_per_second.find(":") + 1:].replace(",", "")
    
    return cookies_per_second

#detects if golden cookie is present and clicks it
def detectGoldenCookie(element: WebElement):
    
    golden_cookie: WebElement = element.find_elements(By.CLASS_NAME, "shimmer")
                
    if(len(golden_cookie) != 0):
            golden_cookie[0].click()

#if notes (or information) can be closed then close it
def closeNotesPopup(element: WebElement):
    
    sub_notes: WebElement = element.find_elements(By.TAG_NAME, "div")
                
    if(len(sub_notes) != 0):
        
        try:
            for i in range(len(sub_notes)):
                if("framed close sidenote" in sub_notes[i].get_attribute("class")):
                    sub_notes[i].click()
        except StaleElementReferenceException:
            sub_notes = element.find_elements(By.TAG_NAME, "div")
  
#returns cookie amount           
def getCookieAmount(element: WebElement) -> float:
    
    cookie_amount = element.text.replace(",", "").split("\n")
                
    if("million" in cookie_amount[0]):
        cookie_amount = float(cookie_amount[0][:cookie_amount[0].find(" million")]) * 1000000
    elif("billion" in cookie_amount[0]):
        cookie_amount = float(cookie_amount[0][:cookie_amount[0].find(" billion")]) * 1000000000
    else:
        cookie_amount = float(cookie_amount[0][:cookie_amount[0].find(" ")])
    
    return cookie_amount

#purchases all available upgrades if cookies is greater than each upgrade cost
def purchaseUpgrades(driver: WebDriver, upgrades: list):
    
    index = 0
    length = len(upgrades)
    
    while index < length:

        try:
            if("enabled" in upgrades[index].get_attribute("class")):
                upgrades[index].click()
            index += 1
        
        except StaleElementReferenceException:
            upgrades = getElement(driver, "//*[@id=\"upgrades\"]//div", True)
            length = len(upgrades)
            index = 0
  
#purchases each product if cookies is greater than each individual product price. Starts from very bottom of products    
def purchaseProducts(driver: WebDriver, element: WebElement, cookie_amount: float, commentsText: WebElement) -> None:
    
    products = getElement(driver, "//*//span[contains(@id, \"productPrice\") and @class=\"price\"]//ancestor::div[contains(@class, \"product\")]", True)  
                
    for i in range(len(products)-1, -1, -1):
    
        if("unlocked" in products[i].get_attribute("class")):
            
            content_div = products[i].find_element(By.CLASS_NAME, "content")
            
            price = str(content_div.find_element(By.CLASS_NAME, "price").text.replace(",", "").split("\n")[0])
            
            if("million" in price):
                price = price[:price.find(" million")]
                price = float(price) * 1000000
            else:
                price = float(price)
                
            if cookie_amount < price: continue
            else:
                
                while cookie_amount >= price:
                    
                    products[i].click()
                    
                    cookie_amount = element.text.replace(",", "").split("\n")
    
                    if("million" in cookie_amount[0]):
                        cookie_amount = float(cookie_amount[0][:cookie_amount[0].find(" million")]) * 1000000
                    elif("billion" in cookie_amount[0]):
                        cookie_amount = float(cookie_amount[0][:cookie_amount[0].find(" billion")]) * 1000000000
                    else:
                        cookie_amount = float(cookie_amount[0][:cookie_amount[0].find(" ")]) 
                    
                    if cookie_amount < price: 
                        upgrades = getElement(driver, "//*[@id=\"upgrades\"]//div", True)
                        break
                
                #after purchase the information for the product is still displayed, so just click on this to hide it
                commentsText.click()  
                
#main function.
def start(clicksPerSecond = 1):
    
    SITE = "https://orteil.dashnet.org/cookieclicker/"
    
    A = Automation().getDriver()
    
    try:
        
        A.get(SITE)
        
        A.implicitly_wait(2)
        
        #cookie
        cookie = getElement(A, "(//*[@id=\"bigCookie\"])")
        
        #holds amount of cookies text and clicks per second text
        output = getElement(A, "//*[@id=\"cookies\"]")
        
        #amount of cookies
        cookie_amount = 0
           
        #products  
        products = getElement(A, "//*//span[contains(@id, \"productPrice\") and @class=\"price\"]//ancestor::div[contains(@class, \"product\")]", True)
        
        #shimmer container (holds golden cookie)
        shimmers = getElement(A, "//*[@id=\"shimmers\"]")
        
        #notes container
        notes = getElement(A, "//*[@id=\"notes\"]")
        
        #list of available upgrades
        upgrades = None
        
        #web cookies popup accept button
        cookies_accpet_button = getElement(A, "/html/body/div[1]/div/a[1]")
        
        cookies_accpet_button.click()
        
        #used to remove ui after last product upgrade
        commentsText = getElement(A, "//*[@id=\"commentsText\"]")
        
        #cookies per second
        cookies_per_second = getCookiesPerSecond(output)
        
        #while cookies less than 10 million run
        while(float(cookie_amount) < 10000000):
        
            try: 
                
                #only clicks if cookies per second is less than 100. Useles afterwards
                if(float(cookies_per_second) < 100):
                    
                    for _ in range(clicksPerSecond):
                        cookie.click()
                    
                    cookies_per_second = getCookiesPerSecond(output)
                    
                #golden cookie
                detectGoldenCookie(shimmers)
                
                #notes popup   
                closeNotesPopup(notes)
                
                #cookie amount
                cookie_amount = getCookieAmount(output)

                #upgrades
                if not upgrades == None:
                    
                    purchaseUpgrades(A, upgrades)
                           
                else:
                    
                    #when cursor is first upgraded, upgrades are added to DOM
                    cursor_upgrade_amount = products[0].find_element(By.CLASS_NAME, "content").find_element(By.ID, "productOwned0").text.split("\n")[0]
                    
                    if len(cursor_upgrade_amount) != 0:
                        if(int(cursor_upgrade_amount) >= 1):
                            upgrades = getElement(A, "//*[@id=\"upgrades\"]//div", True)
                
                #products
                purchaseProducts(A, output, cookie_amount, commentsText)
                upgrades = getElement(A, "//*[@id=\"upgrades\"]//div", True)
                
            #if a click is intercepted report it and continue                    
            except ElementClickInterceptedException as e:
                
                time.sleep(1)
                os.system("cls")
                print(f"\nAN ERROR HAS OCCURED")
                print(f"\nLine {e.__traceback__.tb_lineno}: {e}")
            
            #if an element is no longer interactable report it and continue  
            except ElementNotInteractableException as e:
                
                time.sleep(1)
                os.system("cls")
                print(f"\nAN ERROR HAS OCCURED")
                print(f"\nLine {e.__traceback__.tb_lineno}: {e}")
                
        #clear console and close driver        
        os.system("cls")
        A.quit()
        
    #Handles every other exception unrelated to Selenium
    except Exception as e:
        
        A.quit()
        time.sleep(1)
        os.system("cls")
        print(f"\nAN ERROR HAS OCCURED")
        print(f"\nLine {e.__traceback__.tb_lineno}: {e}")
    
 
#start of execution
if __name__ == "__main__":
    start(200)