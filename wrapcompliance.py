from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import pandas as pd
from io import StringIO

options=webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox');
options.add_argument('--disable-dev-shm-usage');
driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome()
driver.delete_all_cookies()
driver.maximize_window()
print(driver.session_id)
driver.get("https://wrapcompliance.org/en/certification/facility-monitor-list/")
time.sleep(10)

webElement = driver.find_element(By.CSS_SELECTOR, "iframe[title=\"Facilities\"]")
driver.execute_script("arguments[0].scrollIntoView();", webElement)
driver.switch_to.frame(webElement)
webElement = driver.find_element(By.CSS_SELECTOR, "visual-container:nth-child(6) > .bringToFront > .visualContainer > .visualContent > .vcBody > .visualWrapper")
header1=''
header2=''
header3=''
header4=''
header5=''
header6=''
header7=''
header8=''
counter=0
g_json_data=[]
ids_list=[]
thecount=0
tid=''
supp_count=0
lastsupplier=''
lastsuppliercount=0

while True:
   webElement.click()
   dataps=''
   if thecount==0:
       driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
       driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", webElement, "id", "copyrightIcon4")
      
       print(webElement.text)
       dataps=webElement.text
       thecount=thecount+1
   else:
       ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
       ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
       time.sleep(5)
       new_height = driver.execute_script("return document.body.scrollHeight")
      
       webElement = driver.find_element(By.ID, "copyrightIcon4")
       print("_______________________$$$$$")
       #print(webElement.text)
       print(new_height)
       print("_______________________444$$")
       dataps=webElement.text
   p_wrapper=dataps.split("\n")
   #print(p_wrapper)
   print(p_wrapper[0])
   valueCounter=0
   if counter == 0:
       header1=p_wrapper[5]
       header2=p_wrapper[6]
       header3=p_wrapper[7]
       header4=p_wrapper[8]
       header5=p_wrapper[9]
       header6=p_wrapper[10]
       header7=p_wrapper[11]
       header8=p_wrapper[12]
   counter = counter +1
   for tdata in p_wrapper:
      print(tdata.strip())
      if tdata.strip() == "Select Row":
        try:
         data_dict={}
         data_dict["Source Url"]="https://wrapcompliance.org/en/certification/facility-monitor-list/"
         
         header1_data=p_wrapper[valueCounter+1]
         header2_data=p_wrapper[valueCounter+2]
         header3_data=p_wrapper[valueCounter+3]
         header4_data=p_wrapper[valueCounter+4]
         header5_data=p_wrapper[valueCounter+5]
         header6_data=p_wrapper[valueCounter+6]
         header7_data=p_wrapper[valueCounter+7]
         tid=header1_data.strip()
         data_dict[header1]=header1_data.strip()
         data_dict[header2]=header2_data.strip()
         data_dict[header3]=header3_data.strip()
         data_dict[header4]=header4_data.strip()
         data_dict[header5]=header5_data.strip()
         data_dict[header6]=header6_data.strip()
         if header7_data.startswith((' ', '\t')):
            data_dict[header7]=''
            data_dict[header8]=header7_data.strip()
         else:
            data_dict[header7]=header7_data.strip()
            header8_data=p_wrapper[valueCounter+8]
            if header8_data.startswith((' ', '\t')):
               data_dict[header8]=''
            else:
               if header8_data.strip() != "Select Row":
                  data_dict[header8]=header8_data.strip()
               else:
                  data_dict[header8]=''
         #g_json_data.append(data_dict)
         if tid not in ids_list:
            print("%%%%%%%%%%%%%")
            print(tid)
            print("%%%%%%%%%%%%%")
            supp_count = supp_count+1
            ids_list.append(tid)
            g_json_data.append(data_dict)
            lastsuppliercount=0
         else:
            lastsuppliercount = lastsuppliercount + 1
        except:
           break
      valueCounter = valueCounter + 1
   print("-------------------------------------")
   print(tid)
   print(supp_count)
   print(lastsupplier)
   print(lastsuppliercount)
   print("-------------------------------------")
   if lastsuppliercount >40:
      break
print(g_json_data)
json_data = json.dumps(g_json_data, indent=2)

#supp_json_data = json.dumps(g_json_data, indent=2)
driver.quit()
print(json_data)
df_json = pd.read_json(json_data)
df_json.to_excel("wrapcompliance.xlsx")