
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
from shutil import copyfile


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
     

def create_all_regaeton_folder(ipauta_all_folder_path, all_regaeton_path):
    album_folders = os.walk(ipauta_all_folder_path)
    album_folders = list(album_folders)
    for album_folder in album_folders[1:]:
        if album_folder[-1] != []:
            songs = album_folder[-1]
            for song in songs:
                if song[-3:] in ['jpg','txt','db']:
                    continue
                song_path = os.path.join(album_folder[0], song)
                new_song_path = os.path.join(all_regaeton_path, song)
                try:
                    copyfile(song_path, new_song_path)
                except:
                    print(song_path)
                    print('*'*10)
    

        
ipauta_url = 'https://www.ipauta.com/vieja-escuela/'
ipauta_html = requests.get(ipauta_url).text
ipauta_soup = BeautifulSoup(ipauta_html)
ipauta_hrefs = ipauta_soup.find_all('a')
ipauta_hrefs = [ipauta_href.get('href') for ipauta_href in ipauta_hrefs]   
obligao_urls = [ipauta_href for ipauta_href in ipauta_hrefs if ipauta_href.find('obligao') != -1]

     
driver_path = os.path.join(os.getcwd(),'chromedriver.exe')
for url in obligao_urls[710:]:
    print(url, obligao_urls.index(url))
    driver = start_url_driver(url, driver_path, is_headless=False)
    download = driver.find_element_by_class_name('bicon')
    download.click()
    while check_downloads_chrome(driver)==[]:
        pass
    time.sleep(1)
    driver.close()
    
# Remove duplicates (24) (1)

create_all_regaeton = False
ipauta_all_folder_path = r'C:\Users\juan\Downloads\ipauta_all'
all_regaeton_path = r'C:\Users\juan\Downloads\all_regaeton'
if create_all_regaeton:
    create_all_regaeton_folder(ipauta_all_folder_path, all_regaeton_path)
