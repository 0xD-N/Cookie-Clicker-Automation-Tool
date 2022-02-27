import Automation
import time


if __name__ == "__main__":
    
    SITE = "https://orteil.dashnet.org/cookieclicker/"

    A = Automation.Automation()
    A.getSite(SITE)

    A.exit()


#in the div with dash-center class, it's contents are empty until the countdown of the game begins
#then we wait 3 seconds before typing again
#class="dash-letter is-correct is-typed"
#class="dash-letter is-waiting"