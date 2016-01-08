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

def getImageinfo():
	browser=webdriver.Firefox()
	browser.get("https://twitter.com/search?q=nike&src=typd&vertical=default&f=images")
	browser.wait = WebDriverWait(browser, 15)

	tweet_urls=browser.find_elements_by_class_name("AdaptiveStreamGridImage")
	for l in tweet_urls:
		user_id=l.get_attribute("data-user-id")
		tweet_url=l.get_attribute("data-permalink-path")
		tweet_url="https://twitter.com"+tweet_url
		print user_id+' :'+tweet_url
		browser.close()
##getImageinfo()

def getdetail(url):
	browser=webdriver.Firefox()
	browser.get(url)
	browser.wait = WebDriverWait(browser, 15)

	tweet_text=browser.find_element_by_class_name('TweetTextSize--28px').get_attribute('textContent')
	tweet_text=re.sub(r'pic.twitter.com.*', " ", tweet_text)
	username=browser.find_element_by_css_selector('div.permalink-header strong.fullname').get_attribute('textContent')
	username=re.sub(r'Verified account', " ", username)
	retweet=browser.find_element_by_css_selector('a.request-retweeted-popup strong').get_attribute('textContent')
	favorite=browser.find_element_by_css_selector('a.request-favorited-popup strong').get_attribute('textContent')
	date=browser.find_element_by_css_selector('span.metadata span').get_attribute('textContent')
	img_url=browser.find_element_by_css_selector('a.media img').get_attribute("src")
	print tweet_text+'\nUsername: '+username+'\nRetweet:'+retweet+'\nfavorite: '+favorite+'\nDate:'+date+'\nimageUrl:'+img_url
	browser.close()

url=sys.argv[1]
getdetail(url)
#getdetail-->https://twitter.com/BrianSozzi/status/626316445853589504