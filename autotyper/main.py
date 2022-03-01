from selenium.webdriver.remote.webelement import WebElement
from Automation.Automation import Automation
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import wget
from bs4 import BeautifulSoup
import time
import os



if __name__ == "__main__":
    
    
    SITE = "http://www.99lime.com/_bak/topics/html-is-easy/"
    
    A = Automation().getDriver()
    
    soup = None
    
    images = []

    with open("test.txt", "r") as f:
    
        images = f.readlines()
    
    try:
        
        A.get(SITE)
        
        soup = BeautifulSoup(f"{A.page_source}", "html.parser")
        output: WebElement = (WebDriverWait(A, 10).until(lambda driver: driver.find_elements(By.TAG_NAME, "img")))
        
        
        with open("test.txt", "w") as f:
            
            for i in range(len(output)):
                f.write(str(output[i].get_attribute("src")+ "\n"))
        
        os.system("cls")
        A.quit()
        
    #Functional. Don't touch this
    except Exception as e:
        
        A.quit()
        time.sleep(1)
        os.system("cls")
        print(f"\nAN ERROR HAS OCCURED")
        print(f"\nLine {e.__traceback__.tb_lineno}: {e}")


#in the div with dash-center class, it's contents are empty until the countdown of the game begins
#then we wait 3 seconds before typing again
#class="dash-letter is-correct is-typed"
#class="dash-letter is-waiting"