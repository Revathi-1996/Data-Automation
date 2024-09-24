import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from io import StringIO

g_json_data=[]
table_data = []

def extract_table_data(driver, table_locator, header_values):
    rows = driver.find_elements(By.XPATH, table_locator + "/tr")
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")[2:-1]
        row_data = {header_values[index]: column.text for index, column in enumerate(columns)}
        row_data["Source Url"]=source_url
        table_data.append(row_data)
    return table_data

options=webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox');
options.add_argument('--disable-dev-shm-usage');
driver = webdriver.Chrome(options=options)
source_url = "https://portal.betterwork.org/transparency/compliance"
driver.get(source_url)
driver.maximize_window()

time.sleep(15)
while True:
    header_locator = "//*[@id='grdSuppliers']/table/thead"
    header = driver.find_element(By.XPATH, header_locator)
    header_columns = header.find_elements(By.TAG_NAME, "th")
    header_values = [header_column.text for index, header_column in enumerate(header_columns) if index > 1 and index != 10]

    table_locator = "//*[@id='grdSuppliers']/table/tbody"
    table_data = extract_table_data(driver, table_locator, header_values)
    g_json_data = json.dumps(table_data, indent=2)
    
    next_button = driver.find_elements(By.XPATH, "//*[@id='grdSuppliers']/div/a[3]")
    if not next_button or 'disabled' in next_button[0].get_attribute('class'):
        #create excel
        break
    next_button[0].click()
    time.sleep(5)
driver.quit()
print(table_data)

df_json = pd.read_json(StringIO(g_json_data))
df_json.to_excel("betterwork.xlsx")