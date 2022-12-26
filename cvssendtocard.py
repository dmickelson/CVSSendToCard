from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# * This script goes through SalesNav Inbox and adds connections to the CRM that are not already in the database
print("Running Send To CVS Card\n")

# *
# * Start the LinkedIn Profile page scrapping
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
    s = Service('C:\\development\SalesNavInboxAddCandidate\chromedriver.exe')
    browser = webdriver.Chrome(service=s, options=chrome_options)
    print("Connected to Chrome Web Driver Service")
except BaseException as ex:
    print("*** Chrome Web Driver is unreachable, did you start the browser session?")
    print(ex)
    exit()

# * Make Sure its the right CVS Page
try:
    browser.find_element(By.XPATH,"span[@class='sc-send-to-card-action']")
    print("Found correct CVS Page")
    print("Working on parsing Add To Cards")
except NoSuchElementException as ex:
    print ("CVS Element not found")
    print (ex)
    exit()


