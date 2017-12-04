import requests
import os
from selenium import webdriver

browser = webdriver.Chrome("webdriver\chromedriver.exe")
hostname = os.environ.get("COMPUTERNAME", "unknown")
url = "http://localhost:5600/#/activity/%s" % hostname
browser.get(url)
