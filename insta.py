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
import post
import user
import json
from selenium.webdriver.support.ui import Select
import traceback
import utils



path_to_chromedriver = '/Users/djisse/Documents/cheerio/chromedriver' # change path as needed
driver = webdriver.Chrome(executable_path = path_to_chromedriver)

def scroll(url):
	try:
		driver.wait = WebDriverWait(driver, 5)
		driver.get(url)
		driver.wait = WebDriverWait(driver, 5)
		print "INSTA:Scrolling to "+url
		box = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".-cx-PRIVATE-Shell__content")))

		bt=driver.find_element_by_css_selector('.-cx-PRIVATE-AutoloadingPostsGrid__moreLink')
		bt.click()
	    
		driver.wait = WebDriverWait(driver, 5)
		for i in range(1,5):
			print "scrolling"
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
		print 'scrolling finish'
		return 1
	except NoSuchElementException,e:
		print 'Error in scrolling of : No need to scroll '+url+' :'
	except TimeoutException,e:
		print 'Time out for '+url+' :'
		return 0

def getImgLink(key):
	try:
		url='https://instagram.com/explore/tags/'+key+'/'
		scroll(url)
		driver.wait = WebDriverWait(driver, 15)
		print "INSTA: Getting image about:"+key
		list_post={
				'posts' :[]
		}

		list_links=[]
		links=driver.find_elements_by_css_selector('a.-cx-PRIVATE-PostsGridItem__root')
		for l in links:
			link=l.get_attribute("href")
			#print link
			image_url=l.find_element_by_tag_name('img').get_attribute('src')
			list_links.append(link)

		for l in list_links:
			curPost=getdetail(l)
			if curPost !=0:
				list_post["posts"].append(curPost.getJSON())

		#print(json.dumps(list_post))
		return list_post
	except TimeoutException,e:
		print 'Time out for '+key+' :'
		return 0

def getUser(username):
	try:
		url='https://instagram.com/'+username+'/'

		driver.wait = WebDriverWait(driver, 5)
		driver.get(url)
		driver.wait = WebDriverWait(driver, 5)

		box = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".-cx-PRIVATE-Shell__content")))
		print "INSTA: Getting data of this user:"+username

		try:
			avatar=driver.find_element_by_css_selector("img.-cx-PRIVATE-ProfilePage__avatar").get_attribute('src')
		except NoSuchElementException,e:
			avatar='none'
		try:
			description=driver.find_element_by_css_selector(".-cx-PRIVATE-ProfilePage__biography").get_attribute("textContent")
		except NoSuchElementException,e:
			description='none'
		try:
			nb_post=driver.find_element_by_css_selector(".-cx-PRIVATE-PostsStatistic__count").get_attribute("textContent")
			nb_post=utils.cleanNumber(nb_post)
		except NoSuchElementException,e:
			nb_post='0'
		try:
			nb_followers=driver.find_element_by_css_selector(".-cx-PRIVATE-FollowedByStatistic__count").get_attribute("textContent")
			nb_followers= utils.cleanNumber(nb_followers)
		except NoSuchElementException,e:
			nb_followers='0'
		try:
			nb_following=driver.find_element_by_css_selector(".-cx-PRIVATE-FollowsStatistic__count").get_attribute("textContent")
			nb_following= utils.cleanNumber(nb_following)
		except NoSuchElementException,e:
			nb_following='0'
		curUser=user.User('instagram',username,'none',avatar,nb_followers,nb_following,nb_post,'0','none',url)
		#print json.dumps(curUser.getJSON())

		return curUser
	except TimeoutException,e:
		print 'Time out for '+username+' :'
		return 0

def getComment(url):
	driver.get(url)
	driver.wait = WebDriverWait(driver, 15)

	box = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".-cx-PRIVATE-Timestamp__root")))

	listComment={
				'comments' :[]
	}

	root=driver.find_elements_by_css_selector('.-cx-PRIVATE-PostInfo__comment')


	for r in root:
		try:
			name=r.find_element_by_css_selector('.-cx-PRIVATE-UserLink__root.-cx-PRIVATE-PostInfo__commentUserLink').get_attribute('textContent')
			text=r.find_element_by_tag_name('span').get_attribute('textContent')
			listComment["comments"].append({'username': name,'text':text})
		except:
			print "This is not a comment."
	return listComment



def getdetail(url):
	try:
		driver.get(url)
		driver.wait = WebDriverWait(driver, 15)

		box = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".-cx-PRIVATE-Timestamp__root")))

		print "INSTA: Getting detail about this post:"+url
		username=driver.find_element_by_css_selector('a.-cx-PRIVATE-UserLink__root').get_attribute('textContent')
		url_profile=driver.find_element_by_css_selector('a.-cx-PRIVATE-UserLink__root').get_attribute('href')
		try:
			number_like=driver.find_element_by_css_selector('.-cx-PRIVATE-PostLikers__likeCount').get_attribute('textContent')
			number_like=utils.cleanNumber(number_like)
		except NoSuchElementException,e:
			root=driver.find_element_by_css_selector('.-cx-PRIVATE-PostLikers__root')
			try:
				number_like=len(root.find_elements_by_css_selector('.-cx-PRIVATE-UserLink__root'))
				number_like=utils.cleanNumber(number_like)
			except NoSuchElementException,e:
				number_like='0'
		try:
			url_image=driver.find_element_by_css_selector(".-cx-PRIVATE-Photo__image").get_attribute("src")
		except NoSuchElementException,e:
			url_image='none'
		try:
			number_Comment=driver.find_elements_by_css_selector('button.-cx-PRIVATE-PostInfo__commentsLoadMoreButton span')
			if(len(number_Comment)==0):
				raise NoSuchElementException('Manual')
			number_Comment=number_Comment[1].get_attribute('textContent')
			number_Comment=utils.cleanNumber(number_Comment)
		except NoSuchElementException,e:
			try:
				number_Comment=driver.find_elements_by_css_selector('.-cx-PRIVATE-PostInfo__comment')
				number_Comment= len(number_Comment)
				number_Comment=utils.cleanNumber(number_Comment)
			except NoSuchElementException,e:
				number_Comment='0'
		try:
	 		date=driver.find_element_by_css_selector('.-cx-PRIVATE-Timestamp__root').get_attribute('title')
	 	except NoSuchElementException,e:
	 		date='none'
	 	try:
	 		root=driver.find_elements_by_css_selector('.-cx-PRIVATE-PostInfo__comment')[0]
	 		name=root.find_element_by_css_selector('.-cx-PRIVATE-UserLink__root.-cx-PRIVATE-PostInfo__commentUserLink').get_attribute('textContent')
	 		if name == username:
	 			text=root.find_element_by_tag_name('span').get_attribute('textContent')
	 		else:
	 			text='none1'
	 	except NoSuchElementException,e:
	 		text='none2'
		#print 'username: '+username+'\nuser Prof: '+url_profile+'\nlike: '+str(number_like)+'\ncomment: '+str(number_Comment)+'\ndate: '+date
		curPost=post.Post('instagram',url_image,text,date,username,url,number_like,number_Comment,0,url_profile)
		#print curPost.getJSON()
		return curPost
	except TimeoutException,e:
		print 'Time out for '+url+' :'
		return 0
def close():
	print "WARNING CLOSING CONNEXION"
	driver.close()