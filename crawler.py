import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
# import pandas as pd
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager
import sshtunnel 
from getFromDB import insertDocument
from getFromDB import getAllHrefs
from getFromDB import insertTargetUrl
from getFromDB import removeTargetUrl
from getFromDB import getAllTargets
import threading
import pytz
from datetime import datetime
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote
# from pyvirtualdisplay import Display
from extractor_phone_email import extractor

DEPTH = 20
STARTING_TIME = '19:00:00'
ENDING_TIME = '06:00:00'
urls = []
new_hrefs= []
hrefs = []
inserted_hrefs = []
DELAY_TIME = 300

def getAllUrls(driver,url,d):
    global urls,new_hrefs,inserted_hrefs
    if(d == DEPTH):
        return
    if('http' not in url):
        move_url = 'https://' + url
    else:
        move_url = url    
    print(move_url)
    driver.get(move_url)
    if(move_url not in hrefs and move_url not in inserted_hrefs):
        print("New URL found : " + move_url)
        inserted_hrefs.append(move_url)
        html = driver.find_element("xpath",'/html')
        text = html.text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        text = text.lower()
        wordList = text.split()
        keywords = []
        counts = []
        #making keywords list and counting 
        for word in wordList:
            if word not in keywords:
                keywords.append(word)
                counts.append(str(wordList.count(word)))
        keywords = ','.join(keywords)
        counts = ','.join(counts)
        myExtractor = extractor.Extractor(text)
        result = myExtractor.get()
        phones = ','.join(result['phones'])
        emails = ','.join(result['emails'])
        urls.append({'link' : move_url,'keywords': keywords,'counts' : counts,'phones' : phones,'emails':emails })
    a_tags = driver.find_elements(By.TAG_NAME,'a')
    need_hrefs = []
    for a_tag in a_tags:
        while(True):
            try:
                href = a_tag.get_attribute('href')
                break
            except:
                continue
        if(href != None):
            if(url in href and href not in new_hrefs and href not in need_hrefs):
                new_hrefs.append(href)
                need_hrefs.append(href)
            
    for href in need_hrefs:
        getAllUrls(driver,href,d+1)
    return 

def check_time():
    #return True
    dt = datetime.now()
    aus_dt = dt.astimezone(pytz.timezone('Australia/Sydney'))
    start_time = datetime.strptime(STARTING_TIME, '%H:%M:%S').time()
    end_time = datetime.strptime(ENDING_TIME, '%H:%M:%S').time()
    time_now = aus_dt.time()
    print('NOW : ' + str(time_now))
    #return True
    return (time_now > start_time or time_now < end_time)

def search(st,en,df,driver):
    
    for i in range(st,en):
        row = df[i]
        # url = row[0]
        url = df[i]
        getAllUrls(driver,url,0)

def main():
    if(__name__ == '__main__'):
        # with Display():
            chrome_options = uc.ChromeOptions()
            chrome_options.add_argument('--disable-gpu')
            # chrome_options.add_argument('--headless')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-setuid-sandbox')
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)
    
            print("Starting first chrome driver")
            driver_1 = uc.Chrome(service=Service(chromedriver_autoinstaller.install()),option=chrome_options)
    
            # driver_1.delete_all_cookies()
            # driver_1.maximize_window()
            # print("Starting second chrome driver")
            driver_2 = webdriver.Chrome(service=Service(chromedriver_autoinstaller.install()))
    
            # driver_2.delete_all_cookies()
            # driver_2.maximize_window()
            # file_path = input("Please insert search url file path : ")
            target_urls = ['https://www.ratemds.com/best-doctors/qld/','https://www.ripoffreport.com/reports/specific_search/australia']
            target_urls = getAllTargets()
            
            length = len(target_urls)
            half = int(length/2)
            print("----Running Crawler---")
            while(True):
                if(True):
                    
                    global hrefs
                    hrefs = []
                    hrefs = getAllHrefs()
    
                    print("Starting Thread 1")
                    # search(0,half,target_urls,driver_1)
                    thread_1 = threading.Thread(target=search,args=(0,half,target_urls,driver_1,))
                    print("Starting Thread 2")
                    thread_2 = threading.Thread(target=search,args=(half,length,target_urls,driver_2,))
                    thread_1.start()
                    thread_2.start()
                    thread_1.join()
                    thread_2.join()
                    insertDocument(urls)
                    sleep(DELAY_TIME)


def insertTarget(target_url):
    results = insertTargetUrl(target_url)
    return results
    
def removeTarget(target_url):
    results = removeTargetUrl(target_url)
    return results
        

main()