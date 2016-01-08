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

def getPost():
	browser=webdriver.Firefox()
	browser.get("https://twitter.com/search?q=nike&src=typd")
	browser.wait = WebDriverWait(browser, 15)

	contents=browser.find_elements_by_css_selector('div.content')
	for l in contents:
		username=l.find_element_by_css_selector('strong.fullname').get_attribute("innerHTML")
		#print username.encode("utf-8")
		profile_url=l.find_element_by_css_selector('a.account-group ').get_attribute("href")
		profile_url="https://twitter.com"+profile_url
		tweet_text=l.find_element_by_css_selector('p.js-tweet-text').get_attribute("textContent")
		#print tweet_text.encode("utf-8")
		date=l.find_element_by_css_selector('small.time a').get_attribute("title")
		#print date
		number_retweet=l.find_element_by_css_selector('button.js-actionRetweet').get_attribute("textContent")
		number_retweet=re.sub(r'\D+', " ", number_retweet)
		number_favorite=l.find_element_by_css_selector('button.js-actionFavorite').get_attribute("textContent")
		number_favorite=re.sub(r'\D+', " ", number_favorite)
		#print number_favorite
		try:
			imageUrl=l.find_element_by_css_selector('div.is-preview img').get_attribute("src")
			#print imageUrl
		except NoSuchElementException:
			print "Not found"
getPost()
#get all post in https://twitter.com/search?q=nike&src=typd