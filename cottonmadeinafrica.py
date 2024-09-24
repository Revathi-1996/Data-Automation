from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
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
# Maximize the browser window
driver.maximize_window()
driver.get('https://cottonmadeinafrica.org/stoffproduzenten/')
next_button = driver.find_element(By.XPATH, '//*[@id="downloads"]/div/div/div[7]/div[3]/div/a/button')
next_button.click();
time.sleep(5)
driver.close()