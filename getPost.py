from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import re
path_to_chromedriver = '/Users/djisse/Documents/cheerio/chromedriver' # change path as needed
#path_to_chromedriver = 'E:\Jibril-Project\8.sephora\chromedriver.exe'
driver = webdriver.Chrome(executable_path = path_to_chromedriver)

def checkPresence(elem):
	try:
		driver.find_element_by_class_name(elem)
		print 'Found!!!'
		return 1
	except:
		print 'Not found'
		return 0

def scroll(url):
    driver.wait = WebDriverWait(driver, 5)
    driver.get(url)
    driver.wait = WebDriverWait(driver, 5)
    box = driver.wait.until(EC.presence_of_element_located((By.ID, "doc")))

    for i in range(1,6):
    	print "scrolling"
    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    	time.sleep(2)
    print 'scrolling finish'
    return 1

def getPost(key):
	url='https://twitter.com/search?q='+key+'&src=typd'
	scroll(url)
	contents=driver.find_elements_by_css_selector('div.content')
	i=0
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
			print "No image"

		line='Post '+str(i)+' : username: '+username+' ; url: '+profile_url+' ; tweet: '+tweet_text+' ; '+date+' ; nb tweet:'+number_retweet+' ; nb_fav: '+number_favorite+' ; '
		print line
		i=i+1

def getAccount(key):
	url='https://twitter.com/search?q='+key+'&src=typd&vertical=default&f=users'
	scroll(url)
	driver.wait = WebDriverWait(driver, 15)

	blogContents=driver.find_elements_by_css_selector('div.ProfileCard ')
	for l in blogContents:
		user_id=l.get_attribute("data-user-id")
		link=l.find_element_by_css_selector('a.ProfileCard-bg').get_attribute("href")
		print user_id+" :"+link


def getProfileInfo(url):
	driver.get(url)
	driver.wait = WebDriverWait(driver, 15)

	twitter_name=driver.find_element_by_class_name("ProfileHeaderCard-nameLink").get_attribute("textContent")
	twitter_img=driver.find_element_by_class_name("ProfileAvatar-image ").get_attribute("src")
	tweet= driver.find_element_by_css_selector("li.ProfileNav-item--tweets span.ProfileNav-value").get_attribute("textContent")
	following=driver.find_element_by_css_selector('li.ProfileNav-item--following span.ProfileNav-value').get_attribute("textContent")
	followers=driver.find_element_by_css_selector('li.ProfileNav-item--followers span.ProfileNav-value').get_attribute("textContent")
	favorite=driver.find_element_by_css_selector('li.ProfileNav-item--favorites span.ProfileNav-value').get_attribute('textContent')
	print twitter_name+": "+twitter_img+': '+tweet+': '+following+': '+followers+': '+favorite+'\n'

def close():
	driver.close()