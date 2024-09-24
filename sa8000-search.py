from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import sys

file_p=sys.argv[1]
options=webdriver.ChromeOptions()
#options.capabilities['browserName']
prefs={"download.default_directory":file_p}
options.add_experimental_option("prefs",prefs);
options.add_argument('--headless=new')
options.add_argument('--no-sandbox');
options.add_argument('--disable-dev-shm-usage');

driver = webdriver.Chrome(options=options)

driver.maximize_window()

url = "https://sa-intl.org/sa8000-search/"
driver.get(url)

search_button_xpath = '//*[@id="search"]/div/button'
search_button = driver.find_element(By.XPATH, search_button_xpath)
search_button.click()
time.sleep(25)

search_export_xpath = '//*[@id="genesis-content"]/article/div/div[1]/div/div/div[5]/a'
search_export = driver.find_element(By.XPATH, search_export_xpath)
search_export.click()
time.sleep(3)

wait = WebDriverWait(driver, 5)
first_name_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input_43_3_3"]')))
first_name_input.send_keys("testfirst")

last_name_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input_43_3_6"]')))
last_name_input.send_keys("testlast")

email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input_43_2"]')))
email_input.send_keys("test@gmail.com")

country_dropdown = driver.find_element(By.XPATH, '//*[@id="input_43_11"]')
country_dropdown.click()

india_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//option[@value="India"]')))
india_option.click()

time.sleep(3)

company_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input_43_4"]')))
company_input.send_keys("testcompany")

stakeholder_dropdown = Select(wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input_43_12"]'))))
stakeholder_dropdown.select_by_value("Auditor")

no_radio_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="choice_43_10_1"]')))
no_radio_button.click()

submit_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="gform_submit_button_43"]')))
submit_button.click()

time.sleep(10)
driver.quit()