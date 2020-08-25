
"""
Created on Sun Aug 23 18:37:02 2020

@author: lokopobit
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import requests
import os

def start_url_driver(url, driver_path, is_headless=True):
    try:
        if is_headless:
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
        else:
            driver = webdriver.Chrome(executable_path=driver_path)
        driver.implicitly_wait(10)
        driver.get(url)
        return driver
    except:
        print('ERROR: LOADING PAGE ', url)
        
        
def check_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        return document.querySelector('downloads-manager')
        .shadowRoot.querySelector('#downloadsList')
        .items.filter(e => e.state === 'COMPLETE')
        .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
        """)
     
        
ipauta_url = 'https://www.ipauta.com/vieja-escuela/'
ipauta_html = requests.get(ipauta_url).text
ipauta_soup = BeautifulSoup(ipauta_html)
ipauta_hrefs = ipauta_soup.find_all('a')
ipauta_hrefs = [ipauta_href.get('href') for ipauta_href in ipauta_hrefs]   
obligao_urls = [ipauta_href for ipauta_href in ipauta_hrefs if ipauta_href.find('obligao') != -1]

     
driver_path = os.path.join(os.getcwd(),'chromedriver.exe')
for url in obligao_urls[514:]:
    print(url, obligao_urls.index(url))
    driver = start_url_driver(url, driver_path, is_headless=False)
    download = driver.find_element_by_class_name('bicon')
    download.click()
    while check_downloads_chrome(driver)==[]:
        pass
    time.sleep(1)
    driver.close()
    
# Remove duplicates (24) (1)
    
