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
browser=webdriver.Firefox()
def getImgLink():
	
	browser.get("https://instagram.com/safirstores/")
	browser.wait = WebDriverWait(browser, 15)

	links=browser.find_elements_by_css_selector('a.-cx-PRIVATE-PostsGridItem__root')
	for l in links:
		link=l.get_attribute("href")
		print link
		image_url=l.find_element_by_tag_name('img').get_attribute('src')
		print image_url
		#browser.close()


##getImgLink()
#we will get https://instagram.com/p/5GxbvjI911/

def getdetail(url):
	fo = open("listComments.csv", "a+")
	
	browser.get(url)
	browser.wait = WebDriverWait(browser, 15)

	
	username=browser.find_element_by_css_selector('a.-cx-PRIVATE-UserLink__root').get_attribute('textContent')
	url_profile=browser.find_element_by_css_selector('a.-cx-PRIVATE-UserLink__root').get_attribute('href')
	date=browser.find_element_by_css_selector('time.-cx-PRIVATE-Timestamp__root').get_attribute('title')
	#img_url=
	print 'username: '+username+'\nuser Prof: '+url_profile+'\ndate: '+date
	try:
		number_like=browser.find_element_by_css_selector('span.-cx-PRIVATE-PostLikers__likeCount span:nth-child(2)').get_attribute('textContent')
		print number_like
	except NoSuchElementException:
		print 'No like'
	try:
		number_Comment=browser.find_element_by_css_selector('button.-cx-PRIVATE-PostInfo__commentsLoadMoreButton span:nth-child(2)').get_attribute('textContent')
		print number_Comment
		browser.find_element_by_css_selector('button.-cx-PRIVATE-PostInfo__commentsLoadMoreButton').click()
		time.sleep(2)
		try:
			browser.find_element_by_css_selector('li.-cx-PRIVATE-PostInfo__comment button').click()
			time.sleep(2)
			try:
				browser.find_element_by_css_selector('li.-cx-PRIVATE-PostInfo__comment button').click()
			except NoSuchElementException:
				print 'No more Comment'

		except NoSuchElementException:
			print 'No More  Comment'

		browser.implicitly_wait(20)
		# allComments=browser.find_elements_by_css_selector('li.-cx-PRIVATE-PostInfo__comment')
		# i=0
		# for l in allComments:
		# 	#print i
		# 	if i>1:
		# 		try:
		# 			comment=l.find_element_by_tag_name('span').get_attribute('textContent')
		# 			print comment.encode('utf-8')
		# 		except NoSuchElementException:
		# 			print "Not found user comment"
		# 	i=i+1
			
	except NoSuchElementException:
		print "Not found"
	try:
		allComments=browser.find_elements_by_css_selector('li.-cx-PRIVATE-PostInfo__comment')
		i=0
		for l in allComments:
			#print i

			if i>1:
				try:
					user_comment=l.find_element_by_css_selector('a.-cx-PRIVATE-PostInfo__commentUserLink').get_attribute('textContent')
					print user_comment.encode('utf-8')
					comment=l.find_element_by_tag_name('span').get_attribute('textContent')
					print comment.encode('utf-8')
					curLine=comment+";"+user_comment+"\n"
					fo.write(curLine)
				except NoSuchElementException:
					print "Not found user comment"
			i=i+1

	except NoSuchElementException:
		print "Not Comment found"



try:
	url=sys.argv[1]
	getdetail(url)
	browser.close()
except:
	browser.close()