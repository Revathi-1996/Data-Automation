from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import pandas as pd
from io import StringIO

g_json_data=[]
header2='Mills & Manufacturers'
header1='Source Url'
def extract_trustuscotton_entity_data(driver, table_xpath,entity_link):
    print(table_xpath)
    # Find and click the next button
    gr_json_data=[]
    # Wait for a few seconds to let the new page load (you may adjust the duration)
    time.sleep(3)
    global header1
    global header2
    # Find the table on the new page
    p_data = driver.find_element("xpath", table_xpath).text
    print(p_data)
    p_wrapper=p_data.split("\n")
    for dat in p_wrapper:
        dict_data={}
        print(dat)
        dict_data[header1]=entity_link
        dict_data[header2]=dat
        g_json_data.append(dict_data)
        
       #     dict_data[header3]=uflpa_entity_link
       #     dict_data[header1]=columns[0].text
       #     dict_data[header2]=columns[1].text
       #     g_json_data.append(dict_data)
    return gr_json_data

def process_trustuscotton_pages(driver, trustuscotton_link, next_button_xpaths):
    combined_data = []
  
    for  next_button_xpath in  next_button_xpaths:
        # Navigate to the supplier page
        driver.get(trustuscotton_link)

        # Store the data for the current supplier
        data_current_trustuscotton = extract_trustuscotton_entity_data(
            driver,
            next_button_xpath,trustuscotton_link
        )
        
       
    return data_current_trustuscotton

# Create a new instance of the Chrome WebDriver
options=webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox');
options.add_argument('--disable-dev-shm-usage');
driver = webdriver.Chrome(options=options)
# Maximize the browser window
driver.maximize_window()

trustuscotton_link = "https://trustuscotton.org/members/" 
next_button_xpaths = []
next_button_xpaths.append("//*[@id='post-7507']/div/div/section[2]/div/div/div/section[4]/div/div[1]/div/div/div/p")
next_button_xpaths.append("//*[@id='post-7507']/div/div/section[2]/div/div/div/section[4]/div/div[2]/div/div[1]/div/p")


process_trustuscotton_pages(driver, trustuscotton_link, next_button_xpaths)
print(g_json_data)
# Close the browser
driver.quit()

# Convert the combined data to a JSON string
json_data = json.dumps(g_json_data, indent=2)
print(json_data)
#df_json = pd.read_json(json_data)
df_json = pd.read_json(StringIO(json_data))
df_json.to_excel("trustuscotton_list.xlsx")