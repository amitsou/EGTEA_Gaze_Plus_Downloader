from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://google.com/")
print(driver.title)
time.sleep(5)
driver.close()




"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import sys

options = Options()
options.headless = True
driver = webdriver.Chrome("/mnt/e/Code_base_Playground/Python_Code_Base/EGTEA_Gaze_Plus_Downloader/src/webdrivers/chromedriver", options=options)
driver.get("https://google.com/")
print(driver.title)

time.sleep(5)
driver.quit()
"""