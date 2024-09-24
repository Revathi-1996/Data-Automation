from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import pandas as pd
from io import StringIO

g_json_data=[]
header1=''
header2=''
header3='Source Url'
def extract_uflpa_entity_data(driver, table_xpath,counts,uflpa_entity_link):
    print(table_xpath)
    # Find and click the next button
    gr_json_data=[]
    # Wait for a few seconds to let the new page load (you may adjust the duration)
    time.sleep(3)
    global header1
    global header2
    # Find the table on the new page
    table = driver.find_element("xpath", table_xpath)
    # Extract data from the table and store it in a list
    #table_data = [f"Supplier Name: {supplier_name}"]
    rows = table.find_elements("tag name", "tr")
    print(counts)
    for row in rows:
        dict_data={}
        if counts == 1:
           headers = row.find_elements("tag name", "th")
           print(headers)
           if headers:
               header1=headers[0].text
               header2=headers[1].text
          # for i in headers:
          #     print(i.text)
        columns = row.find_elements("tag name", "td")
        if columns:
           # dict_data[header3]=uflpa_entity_link
            dict_data[header1]=columns[0].text
            dict_data[header2]=columns[1].text
            g_json_data.append(dict_data)
    return gr_json_data

def process_uflpa_pages(driver, uflpa_links, next_button_xpaths):
    combined_data = []
    counts=1
    for  next_button_xpath in  next_button_xpaths:
        # Navigate to the supplier page
        driver.get(uflpa_links)

        # Store the data for the current supplier
        data_current_uflpa = extract_uflpa_entity_data(
            driver,
            next_button_xpath,counts,uflpa_links
        )
        counts = counts +1
       
    return data_current_uflpa

# Create a new instance of the Chrome WebDriver
options=webdriver.ChromeOptions()
#options.capabilities['browserName']
#prefs={"download.default_directory":"/opt/seleniumcode/"}
#options.add_experimental_option("prefs",prefs);
options.add_argument('--headless=new')
options.add_argument('--no-sandbox');
options.add_argument('--disable-dev-shm-usage');
#options.binary_location='/opt/seleniumcode/chromedriver'
# Create a new instance of the Chrome WebDriver
#service = Service(executable_path='chromedriver')
driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome()

# Maximize the browser window
driver.maximize_window()

uflpa_entity_link = "https://www.dhs.gov/uflpa-entity-list" 
next_button_xpaths = []
next_button_xpaths.append("//*[@id='block-mainpagecontent']/article/div/div[3]/div[1]/div/div/div/div/div/div/div/div/table[1]")
next_button_xpaths.append("//*[@id='block-mainpagecontent']/article/div/div[3]/div[1]/div/div/div/div/div/div/div/div/table[2]")
next_button_xpaths.append("//*[@id='block-mainpagecontent']/article/div/div[3]/div[1]/div/div/div/div/div/div/div/div/table[4]")


process_uflpa_pages(driver, uflpa_entity_link, next_button_xpaths)
print(g_json_data)
# Close the browser
driver.quit()

# Convert the combined data to a JSON string
json_data = json.dumps(g_json_data, indent=2)
print(json_data)
df_json = pd.read_json(StringIO(json_data))
df_json.to_excel("uflpa_entity_list.xlsx",index=False)
