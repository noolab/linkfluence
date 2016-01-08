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
import sys
import utils
reload(sys)
sys.setdefaultencoding("UTF8")

path_to_chromedriver = '/Users/djisse/Documents/cheerio/chromedriver' # change path as needed
driver = webdriver.Chrome(executable_path = path_to_chromedriver)

txtEmail='litakeo@yahoo.com'
txtPass= '12345Lita'

def connect():
	driver.get("https://www.facebook.com/")
	try:
		box3 = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fbxWelcomeBoxName")))
		print "Already connected!"
		return 1
	except:
		print "Connection to facebook.com"
	
	
	try:
		box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "firstname")))

		firstname=driver.find_element_by_css_selector("form#login_form input#email")
		firstname.send_keys(txtEmail);
		email=driver.find_element_by_css_selector("form#login_form input#pass")
		email.send_keys(txtPass)
		try:
			#submit=driver.find_element_by_id("u_0_x")
			submit=driver.find_elements_by_tag_name('input')[3]
			submit.click()
		except NoSuchElementException:
			print "button not found"
			return 0

		box2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fbxWelcomeBoxName")))
		return 1
	except NoSuchElementException,e:
		print "Error in getting element!"
		return 0
	except TimeoutException,e:
		print 'Time out for '
		return 0


def getComment(url):
	connect()
	driver.get(url)
	comments=driver.find_elements_by_css_selector("li.UFIRow.UFIComment.display.UFIComponent")
	commentaire={
		'comments':[]
	}
	for c in comments:
		try:
			avatar=c.find_element_by_css_selector("._ohe.lfloat .UFIImageBlockImage .UFIActorImage").get_attribute('src')
		except NoSuchElementException,e:
			avatar='none'
		try:
			username=c.find_element_by_css_selector("div.UFICommentContent a").text
		except NoSuchElementException,e:
			username='none'
		try:
			profile=c.find_element_by_css_selector("div.UFICommentContent a").get_attribute("href")
		except NoSuchElementException,e:
			profile='none'
		try:
			text=c.find_element_by_css_selector(".UFIImageBlockContent span.UFICommentBody").get_attribute("textContent")
		except NoSuchElementException,e:
			text='none'
		try:
			date=c.find_element_by_css_selector(".UFIImageBlockContent .livetimestamp").get_attribute("data-utime")
		except NoSuchElementException,e:
			'none'
		commentaire["comments"].append({
					'avatar' : avatar,
					'username':username,
					'profile':profile,
					'text': text,
					'date': date
				})
	#print json.dumps(commentaire)
	return commentaire


def login(keyword):
	list_post={
			'posts' :[]
	}
	print "FB: Search about "+keyword
	connect()
	#Login finish
	newUrl="https://www.facebook.com/search/str/"+keyword+"/keywords_top"
	driver.get(newUrl)
	box3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "._43o4")))

	for i in range(10):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2)
	contents=driver.find_elements_by_css_selector('div.userContentWrapper._5pcr')#('div._1dwg')

	for l in contents:
		try:
			try:
				username=l.find_element_by_css_selector('.fwn.fcg a').get_attribute('textContent')
			except NoSuchElementException:
				username='no username'
			try:
				profile_url=l.find_element_by_css_selector('.fwn.fcg a').get_attribute('href')
			except NoSuchElementException:
				profile_url="no url"
			try:
				userContent=l.find_element_by_css_selector('div._5pbx.userContent').get_attribute('textContent')
			except NoSuchElementException:
				userContent="no content"
			try:
				date=l.find_element_by_css_selector("._5ptz").get_attribute("data-utime")
			except:
				date="no date"
			try:
				img_url=l.find_element_by_css_selector('img.scaledImageFitWidth').get_attribute('src')
			except NoSuchElementException:
				#try:
				#	img_url=l.find_element_by_css_selector('._46-i.img').get_attribute('src')
				#	link=l.find_element_by_css_selector('._46-i.img').get_attribute('href')
				#except NoSuchElementException:
				img_url="no image"
			try:
				link=l.find_elements_by_css_selector('.mtm a')
				if len(link)>0:
					link=link[0].get_attribute('href')
				else:
					link="no link"
			except NoSuchElementException:
				link="no link"
			try:
				info_likes=l.find_element_by_css_selector("div._3ty9 span a")
				info_likes=info_likes.get_attribute("aria-label").split(' ')

				try:
					likes=info_likes[0]
					likes=utils.cleanNumber(likes)
				except IndexError:
					likes='0-'

				try:
					comments=info_likes[2]
					comments=utils.cleanNumber(comments)
				except IndexError:
					comments='0-'
				try:
					share=info_likes[4]
					share=utils.cleanNumber(share)
				except IndexError:
					share='0-'

			except NoSuchElementException:
				likes='0'
				comments='0'
				share='0'
			curPost=post.Post('facebook',img_url,userContent,date,username,link,likes,comments,share,profile_url)
			list_post["posts"].append(curPost.getJSON())
			#getUser(profile_url)
		except NoSuchElementException:
			print "element not found"
			return 0
	return list_post

def getUser(url):
	print "FB: Getting data about this user: "+url
	connect()
	driver.get(url)
	box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".profilePic.img")))

	username=driver.title.split(" | ")[0]

	try:
		avatar=driver.find_element_by_css_selector('.profilePic.img').get_attribute("src")
	except NoSuchElementException,e:
		avatar="no avatar"
	try:
		a=driver.find_element_by_partial_link_text("a friend request.")
		nb_followers=driver.find_element_by_css_selector("span._71u .uiLinkSubtle").text
	except NoSuchElementException,e:
		try:
			nb_followers=driver.find_elements_by_css_selector("tr._51mx a.uiLinkSubtle")[0].text
		except:
			nb_followers='0'
	if nb_followers.find("people") != -1:
		ind=nb_followers.find("people")
		nb_followers=nb_followers[0:ind-1]
		nb_followers=utils.cleanNumber(nb_followers)
	try:
		location=driver.find_element_by_css_selector("._2kcr._42ef").text
	except NoSuchElementException,e:
		location='no location'
	#print "NB FOLLOWERS A LA SOURCE="+str(nb_followers)
	curUser=user.User('facebook',username,'none',avatar,nb_followers,'0','0','0','none',url)
	return curUser


def close():
	driver.close()