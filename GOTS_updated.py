from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import pandas as pd
from io import StringIO

def get_by_label(driver, label):
    xpath = f"//a[contains(., '{label}')]"
    return driver.find_element(By.XPATH, xpath)


#driver = webdriver.Chrome()
#driver.maximize_window()
#driver = webdriver.Chrome()
options=webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox');
options.add_argument('--disable-dev-shm-usage');
driver = webdriver.Chrome(options=options)
driver.maximize_window()
actions = ActionChains(driver)
driver.get("https://global-standard.org/find-suppliers-shops-and-inputs/certified-suppliers/database/search_results")

link_element = driver.find_element(By.XPATH, '//*[@id="xFormA-0"]')
link_element.click()
driver.implicitly_wait(10)
content_element = driver.find_element(By.XPATH, '//*[@id="xFormForm-0-submit"]')
driver.execute_script("arguments[0].click();", content_element)
time.sleep(10)
cookie_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/a[2]')
actions.move_to_element(cookie_element).perform()
cookie_element.click()
time.sleep(10)

all_button = driver.find_element(By.XPATH, '//*[@id="element-xFormAjaxTable-0"]/div[3]/a[1]')
actions.move_to_element(all_button).perform()
all_button.click()

time.sleep(120)
json_data = []

# Extracting data from the table
table_element = driver.find_element(By.XPATH, '//*[@id="tr-xFormAjaxTable-0"]/table')
rows = table_element.find_elements(By.TAG_NAME, 'tr')[1:]
counter=1
for row in rows:
    columns = row.find_elements(By.TAG_NAME, 'td')
    supplier_name = columns[0].text.strip() 
    page_data = {"Source URL": driver.current_url, "Supplier Name": supplier_name}
    link_to_next_page = driver.find_element(By.XPATH,'//*[@id="tr-xFormAjaxTable-0"]/table/tbody/tr['+str(counter)+']/td[5]/a')
    driver.execute_script("arguments[0].click();", link_to_next_page)
    time.sleep(5)
    xpath_value_element = driver.find_element(By.XPATH, '//*[@id="xFormH1-0"]')
    supplier_names = xpath_value_element.text.strip()
    print(supplier_names)
    for j in range(4):
        try:
            additional_xpath_element = driver.find_element(By.XPATH, f'//*[@id="xFormH3-{j}"]')
            table_element = driver.find_element(By.XPATH, f'//*[@id="xFormTable-{j}"]/tbody')
            rows = table_element.find_elements(By.TAG_NAME, 'tr')
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, 'th')
                data_columns = row.find_elements(By.TAG_NAME, 'td')
                for header, data in zip(columns, data_columns):
                    page_data[header.text.strip()] = data.text.strip()
        except NoSuchElementException:
            print("NO data here")
    print(json.dumps(page_data, indent=2))
    json_data.append(page_data)

    time.sleep(5)
    driver.back()
    print(counter)
    counter=counter+1
driver.quit()
json_data = json.dumps(json_data, indent=2)
print(json_data)
df_json = pd.read_json(json_data)
df_json.to_excel("GOTS.xlsx")
print("_______________________")