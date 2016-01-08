import time
import io
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import selenium
import selenium 
import re
from selenium.webdriver.support.ui import Select
reload(sys)
sys.setdefaultencoding("UTF8")

def getAccount():
	browser=webdriver.Firefox()
	browser.get("https://twitter.com/search?q=nike&src=typd&vertical=default&f=users")
	browser.wait = WebDriverWait(browser, 15)

	blogContents=browser.find_elements_by_css_selector('div.ProfileCard ')
	for l in blogContents:
		user_id=l.get_attribute("data-user-id")
		link=l.find_element_by_css_selector('a.ProfileCard-bg').get_attribute("href")
		print user_id+" :"+link


#getAccount()
def getProfileInfo(url):
	browser=webdriver.Firefox()
	browser.get(url)
	browser.wait = WebDriverWait(browser, 15)

	twitter_name=browser.find_element_by_class_name("ProfileHeaderCard-nameLink").get_attribute("textContent")
	twitter_img=browser.find_element_by_class_name("ProfileAvatar-image ").get_attribute("src")
	tweet= browser.find_element_by_css_selector("li.ProfileNav-item--tweets span.ProfileNav-value").get_attribute("textContent")
	following=browser.find_element_by_css_selector('li.ProfileNav-item--following span.ProfileNav-value').get_attribute("textContent")
	followers=browser.find_element_by_css_selector('li.ProfileNav-item--followers span.ProfileNav-value').get_attribute("textContent")
	favorite=browser.find_element_by_css_selector('li.ProfileNav-item--favorites span.ProfileNav-value').get_attribute('textContent')
	print twitter_name+": "+twitter_img+': '+tweet+': '+following+': '+followers+': '+favorite+'\n'
	browser.close()
	
url=sys.argv[1]
getProfileInfo(url)
#getProfileInfo-->https://twitter.com/Nike