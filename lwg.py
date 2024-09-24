from selenium import webdriver
import time
import json
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from io import StringIO
from datetime import datetime
import validators


g_json_data = []

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def extract_supplier_data(driver, next_button_xpath, supplier_name_xpath, table_xpath, div_wrapper_standard_xpath):
    next_button = driver.find_element("xpath", next_button_xpath)
    driver.execute_script("arguments[0].scrollIntoView();", next_button)
    next_button.click()
    dict_data = {}
    time.sleep(3)
    supplier_name = driver.find_element("xpath", supplier_name_xpath).text
    dict_data["facility"] = supplier_name
    table = driver.find_element("xpath", table_xpath)
    rows = table.find_elements("tag name", "tr")
    dict_data["sourceUrl"]=driver.current_url
    for row in rows:
        columns = row.find_elements("tag name", "td")
        col_name=''
        colnam=columns[0].text
        if colnam == 'Rating':
           col_name='rating'
           dict_data[col_name] = columns[1].text
        if colnam == 'Leather Types':
           col_name='leatherTypes'
           dict_data[col_name] = columns[1].text
        if colnam == 'Tannage Types':
           col_name='tannageTypes'
           dict_data[col_name] = columns[1].text
        if colnam == 'Animal Types':
           col_name='animalTypes'
           dict_data[col_name] = columns[1].text
        if colnam == 'Industries Supplied':
           col_name='industriesSupplied'
           dict_data[col_name] = columns[1].text
        if colnam == 'Protocol Issue':
           col_name='protocolIssue'
           dict_data[col_name] = columns[1].text
        if colnam == 'Auditor':
           col_name='auditor'
           dict_data[col_name] = columns[1].text
        if colnam == 'Audit Category':
           col_name='auditCategory'
           dict_data[col_name] = columns[1].text
        if colnam == 'Audit Expiry Date':
           col_name='auditExpiryDate'
           exp=columns[1].text
           tdate=datetime.strptime(exp, '%d %B %Y')
           date_obj = tdate.strftime("%b %d, %Y")
          # rtdate=datetime.strptime(date_obj, "%d/%m/%Y")
           dict_data[col_name] = date_obj
        if colnam == 'Physical Traceability':
           col_name='physicalTraceability'
           sub=columns[1].text
           dict_data[col_name] = sub.replace('%%', '%').replace('N/A%', '')
        if colnam == 'Documented Traceability':
           col_name='documentTraceability'
           sub=columns[1].text
           dict_data[col_name] = sub.replace('%%', '%').replace('N/A%', '')
        if colnam == 'Group Traceability':
           col_name='groupTraceability'
           sub=columns[1].text
           dict_data[col_name] = sub.replace('%%', '%').replace('N/A%', '')
        if colnam == 'Regional Traceability':
           col_name='regionalTraceability'
           sub=columns[1].text
           dict_data[col_name] = sub.replace('%%', '%').replace('N/A%', '')
        if colnam == 'Not Traceable':
           col_name='nonTraceable'
           sub=columns[1].text
           dict_data[col_name] = sub.replace('%%', '%').replace('N/A%', '')
        if colnam == 'Subcontractor score':
           col_name='subcontractorScore'
           sub=columns[1].text
           da=sub.split("%")[0]
           if isfloat(da):
               dict_data[col_name] = da
           
    count = 1
    while True:
        try:
            xpathd = div_wrapper_standard_xpath + "/p[" + str(count) + "]"
            div_wrapper_standard1 = driver.find_element("xpath", xpathd).text
            p_wrapper = div_wrapper_standard1.split("\n")
            if p_wrapper[0] == 'Contact':
               col_name='contact'
               dict_data[col_name] = p_wrapper[1]
            if p_wrapper[0] == 'Email':
               col_name='email'
               dict_data[col_name] = p_wrapper[1]
            if p_wrapper[0] == 'Phone number':
               col_name='phoneNumber'
               dict_data[col_name] = p_wrapper[1]
            if p_wrapper[0] == 'Site Address':
               col_name='siteAddress'
               dict_data[col_name] = p_wrapper[1]
            if p_wrapper[0] == 'URN':
               col_name='urn'
               dict_data[col_name] = p_wrapper[1]
            if p_wrapper[0] == 'Type':
               col_name='type'
               dict_data[col_name] = p_wrapper[1]
            if p_wrapper[0] == 'Continuously Certified Since':
               col_name='continuouslyCertifiedSince'
               exp=p_wrapper[1]
               tdate=datetime.strptime(exp, '%d %B %Y')
               date_obj = tdate.strftime("%b %d, %Y")
               dict_data[col_name] = date_obj
            count += 1
        except:
            break
    try:
       website_element = driver.find_element(By.XPATH, "//*[@id='c4220']/div/div/div/div/div/div[2]/div/div[2]/a")
       website_data=website_element.get_attribute('href')
       if validators.url(website_data):
           dict_data['website'] = website_data
       else:
           dict_data['website']=''
    except:
       #print('no website')
       dict_data['website']=''
    dict_data['fleshDropSplits']=''
    dict_data['hidesTopGrainSplits']=''
    dict_data['hidesFullSubstances']=''
    dict_data['skins']=''
    return dict_data

def process_page(driver, next_button_xpaths_template):
    combined_data = []
    entries_found = False
    for j in range(1, 13):
        next_button_xpath = next_button_xpaths_template.format(index=j)
        try:
            data_next_page = extract_supplier_data(
                driver,
                next_button_xpath,
                "//*[@id='top']/header/div[2]/div[2]/h1/span",
                "//*[@id='c4220']/div/div/div/div/div/div[1]/div",
                "//*[@id='c4220']/div/div/div/div/div/div[2]/div/div/div",
            )
            combined_data += data_next_page
           # print(data_next_page)
            json_data_next_page = json.dumps(data_next_page, indent=2)
           # print(json_data_next_page)
            if 'auditExpiryDate' in data_next_page:
                g_json_data.append(data_next_page)
                
           # print(json_data_next_page)
            entries_found = True
        except NoSuchElementException:
            print("No more entries found on the page.")
            break
        driver.back()
        time.sleep(3)
    return combined_data if entries_found else None

def process_additional_page(driver, next_button_xpath_additional, next_button_xpaths_template):
    combined_data = []
    try:
        iteration = 0
        entries_found = False
        while True:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, next_button_xpath_additional))
            )
            next_button_additional = driver.find_element(By.XPATH, next_button_xpath_additional)
            next_button_additional.click()
            time.sleep(3)
            additional_data = process_page(driver, next_button_xpaths_template)
            if not additional_data:
                print("No more entries found on additional page.")
                break
            combined_data += additional_data
            entries_found = True
            iteration += 1
    except (NoSuchElementException, TimeoutException):
        if not entries_found:
            print("Next button not found. End of the page!!!!")
    return combined_data if entries_found else None

def extract_and_process_page(driver, next_button_xpaths_template, index_range, supplier_links, additional_xpaths):
    combined_data = []
    for supplier_link in supplier_links:
        driver.get(supplier_link)

        data_page = process_page(driver, next_button_xpaths_template)
        if not data_page:
            break  # No more entries found on the main page
        
        for additional_xpath in additional_xpaths:
             additional_data = process_additional_page(driver, additional_xpath, next_button_xpaths_template)
             if not additional_data:
                 break  # No more entries found on the additional pages
             combined_data += additional_data
    return combined_data

options=webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox');
options.add_argument('--disable-dev-shm-usage');
driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome()
driver.maximize_window()
single_supplier_link = "https://www.leatherworkinggroup.com/get-involved/our-community/certified-suppliers"
next_button_xpaths_template = "//*[@id='c4672']/div/div/div[2]/div[{index}]/div[2]/h2/a"
additional_xpaths = [
    "//a[contains(@href, '/get-involved/our-community/certified-suppliers/') and contains(text(), 'Next')]",
]
supplier_links = [single_supplier_link]
combined_data = extract_and_process_page(driver, next_button_xpaths_template, range(1, 13), supplier_links, additional_xpaths)
driver.quit()
json_data = json.dumps(g_json_data, indent=2)
print(json_data)
df_json = pd.read_json(StringIO(json_data))
current_time = datetime.now()
filen=str(current_time.day)+"-"+str(current_time.month)+"-"+str(current_time.year)+"_LWG.xlsx"
with pd.ExcelWriter(filen) as writer:
    df_json.to_excel(writer, sheet_name='LWG_DATA',index=False)