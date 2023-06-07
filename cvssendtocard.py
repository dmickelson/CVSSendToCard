import time
import logging
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


logger = logging.getLogger("CVSSendToCard")
logger.setLevel(logging.INFO)
# * create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt="%(asctime)s: %(name)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")
# * add formatter to ch
ch.setFormatter(formatter)
# * add ch to logger
logger.addHandler(ch)  


# * This script goes through SalesNav Inbox and adds connections to the CRM that are not already in the database
logger.info("Running Send To CVS Card\n")
# ? CVS URL https://www.cvs.com/extracare/home

# *
# * Start the CVS Page Button clicking!
# *
# * Start a new chrome browser session
# ? Reuse existing browser MACOS: Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"
# ? MACOS: To authorize new downloaded chromedriver. Open Terminal window and chromedriver location and type xattr -d com.apple.quarantine chromedriver
# ? Windows: start chrome.exe -–remote-debugging-port=9222 --user-data-dir="C:/temp" 
# ? Windows: Manually create the C:/temp directory
# ? Be sure to Log Into LinkedIn first
# ? Be sure to also add the LinkMatch extension as well to check Zoho Recruit

try:
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-ssl-errors')   
    # * Specifies the path to the chromedriver.exe
    # * MAC OS Location
    # s = Service('/Users/david/projects/LinkedInProfileEval/chromedriver')
    # * WINDOWS OS Location
    s = Service('C:\Program Files (x86)\Chromedriver\chromedriver.exe')
    browser = webdriver.Chrome(service=s, options=chrome_options)
    logger.info("Connected to Chrome Web Driver Service")
except BaseException as ex:
    logger.exception("*** Chrome Web Driver is unreachable, did you start the browser session?")
    logger.exception(ex)
    exit()

# * Make Sure its the right CVS Page
try:
    browser.find_element(By.XPATH,"//h1[contains(@id,'extracareHeading')]")
    # browser.find_element(By.XPATH,"//span[contains(@class,'sc-send-to-card-action')]")
    logger.debug("Found correct CVS Page")
    logger.debug ("Scrolling to end of page to load all Send To Card Elements")
    browser.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
    time.sleep(1)
    logger.info("Working on finding Coupons")
    logger.debug("Coupons found: " + str(len(browser.find_elements(By.XPATH,"//span[text()='Send to card']"))))
    # if (browser.find_element(By.XPATH,"//span[text()='Send to card']")):
    try: 
        while (browser.find_element(By.XPATH,"//span[text()='Send to card']")):
            coupons_left = len(browser.find_elements(By.XPATH,"//span[text()='Send to card']"))
            logger.info("Coupons left: " + str(coupons_left))
            # sendToCard = browser.find_element(By.XPATH,"//span[text()='Send to card']")
            # sendToCard = browser.find_element(By.XPATH,"//button[contains(@class,'sc-send-to-card-action')]")
            sendToCard = browser.find_element(By.XPATH,"//span[contains(@class,'sc-send-to-card-action')]")
            browser.execute_script("arguments[0].click();", sendToCard)
            if coupons_left == 1:
                # One final browse to end of page to handle dynamic loading
                logger.debug ("Scrolling to end of page one last time")
                browser.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
            time.sleep(0.5) # half a second
    except NoSuchElementException as ex:
        logger.info ("No more send to card elements found. All Done!")
        exit()
        
except NoSuchElementException as ex:
    logger.exception ("CVS Element not found")
    logger.exception (ex)
    exit()



