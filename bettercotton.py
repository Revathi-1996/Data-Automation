from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import sys

file_p=sys.argv[1]
options=webdriver.ChromeOptions()
#options.capabilities['browserName']
prefs={"download.default_directory":file_p}
options.add_experimental_option("prefs",prefs);
options.add_argument('--headless=new')
options.add_argument('--no-sandbox');
options.add_argument('--disable-dev-shm-usage');
#options.binary_location='/opt/seleniumcode/chromedriver'
# Create a new instance of the Chrome WebDriver
service = Service(executable_path='chromedriver')
driver = webdriver.Chrome(options=options)
action = ActionChains(driver);
# Maximize the browser window
driver.maximize_window()
driver.get('https://bettercotton.org/membership/find-members/')
time.sleep(5)
gotit=driver.find_element(By.XPATH,'//*[@id="moove_gdpr_cookie_info_bar"]/div/div/div[2]/button[1]');
gotit.click();
next_button = driver.find_element(By.XPATH, '//*[@id="aside"]/div/div[2]/a/i')
time.sleep(5)
#next_button.click();
action.move_to_element(next_button).perform()
next_button.click();
time.sleep(5)
driver.close()