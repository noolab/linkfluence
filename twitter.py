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
import json
import datetime
import traceback
path_to_chromedriver = '/Users/djisse/Documents/cheerio/chromedriver' # change path as needed
import post
import user
import utils
reload(sys)

sys.setdefaultencoding("UTF8")
#path_to_chromedriver = 'E:\Jibril-Project\8.sephora\chromedriver.exe'
driver = webdriver.Chrome(executable_path = path_to_chromedriver)

driver.wait = WebDriverWait(driver, 5)

def checkPresence(elem):
	try:
		driver.find_element_by_class_name(elem)
		print 'Found!!!'
		return 1
	except:
		print 'Not found'
		return 0

def scroll(url):
	try:
	    driver.wait = WebDriverWait(driver, 5)
	    driver.get(url)
	    driver.wait = WebDriverWait(driver, 5)
	    box = driver.wait.until(EC.presence_of_element_located((By.ID, "doc")))

	    for i in range(1,10):
	    	print "scrolling"
	    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	    	time.sleep(2)
	    print 'scrolling finish'
	    return 1
	except NoSuchElementException,e:
		print 'Error in scrolling of '+url+' :'
		print(traceback.format_exc())
	except TimeoutException,e:
		print 'Sroll: Time out for '+url+' :'

def getElementAttr(selector,attr,parent):
	try:
		elt=parent.find_element_by_css_selector(selector).get_attribute(attr)
		return elt
	except NoSuchElementException,e:
		print "element not found: "+selector
		return "-1"


def getPost(key):
	try:
		print "Twitter: Getting list of post about : "+key
		url='https://twitter.com/search?q='+key+'&src=typd'
		scroll(url)

		contents=driver.find_elements_by_css_selector('div.content')
		i=0
		list_post={
			'posts' :[]
		}
		print "CURRENT URL="+url
		for l in contents:
			username=getElementAttr('.username b',"textContent",l)
			#print username.encode("utf-8")
			profile_url=getElementAttr('a.account-group ',"href",l)
			tweet_text=getElementAttr('p.js-tweet-text','textContent',l)
			#print tweet_text.encode("utf-8")

			try:
				url_post=l.find_element_by_css_selector(".time a").get_attribute("href")
			except NoSuchElementException:
				url_post="No url"
			try:
				span=l.find_element_by_css_selector("._timestamp.js-short-timestamp")
				print "Element date found"
				date=span.get_attribute("data-time")
				print "Attribute date found "+date
				date=datetime.datetime.fromtimestamp(int(date)).strftime('%d-%m-%Y %H:%M:%S')
			except NoSuchElementException:
				date="-2"
			#print date
			try:
				number_retweet=l.find_element_by_css_selector('button.js-actionRetweet').get_attribute("textContent")
				number_retweet=re.sub(r'\D+', " ", number_retweet)
				number_retweet=utils.cleanNumber(number_retweet)
			except NoSuchElementException,e:
				number_retweet='0'
			
			try:
				number_favorite=l.find_element_by_css_selector('button.js-actionFavorite').get_attribute("textContent")
				number_favorite=re.sub(r'\D+', " ", number_favorite)
				number_favorite=utils.cleanNumber(number_favorite)
			except NoSuchElementException,e:
				number_favorite='0'
			#print number_favorite
			try:
				imageUrl=l.find_element_by_css_selector('div.is-preview img').get_attribute("src")
			except NoSuchElementException:
				imageUrl='none'

			#line='Post '+str(i)+' : username: '+username+' ; url: '+profile_url+' ; tweet: '+tweet_text+' ; '+date+' ; nb tweet:'+number_retweet+' ; nb_fav: '+number_favorite+' ; '
			#print line
			i=i+1
			print "url="+url_post
			print "profile="+profile_url
			curPost= post.Post('twitter',imageUrl,tweet_text,date,username,url_post,number_favorite,0,number_retweet,profile_url)
			list_post["posts"].append(curPost.getJSON())
		#print(json.dumps(list_post))
		return list_post
	except NoSuchElementException,e:
		print 'Error in getDetail of '+key+' :'
		print(traceback.format_exc())
		return 0
	except TimeoutException,e:
		print 'Time out for '+url+' :'
		return 0

def getPostInstant(key):
	try:
		print "Twitter: Getting list of post about : "+key
		url='https://twitter.com/search?f=tweets&vertical=default&q='+key+'&src=typd'
		scroll(url)

		contents=driver.find_elements_by_css_selector('div.content')
		i=0
		list_post={
			'posts' :[]
		}
		print "CURRENT URL="+url
		for l in contents:
			username=getElementAttr('.username b',"textContent",l)
			#print username.encode("utf-8")
			profile_url=getElementAttr('a.account-group ',"href",l)
			tweet_text=getElementAttr('p.js-tweet-text','textContent',l)
			#print tweet_text.encode("utf-8")

			try:
				url_post=l.find_element_by_css_selector(".time a").get_attribute("href")
			except NoSuchElementException:
				url_post="No url"
			try:
				span=l.find_element_by_css_selector("._timestamp.js-short-timestamp")
				print "Element date found"
				date=span.get_attribute("data-time")
				print "Attribute date found "+date
				date=datetime.datetime.fromtimestamp(int(date)).strftime('%d-%m-%Y %H:%M:%S')
			except NoSuchElementException:
				date="-2"
			#print date
			try:
				number_retweet=l.find_element_by_css_selector('button.js-actionRetweet').get_attribute("textContent")
				number_retweet=re.sub(r'\D+', " ", number_retweet)
				number_retweet=utils.cleanNumber(number_retweet)
			except NoSuchElementException,e:
				number_retweet='0'
			
			try:
				number_favorite=l.find_element_by_css_selector('button.js-actionFavorite').get_attribute("textContent")
				number_favorite=re.sub(r'\D+', " ", number_favorite)
				number_favorite=utils.cleanNumber(number_favorite)
			except NoSuchElementException,e:
				number_favorite='0'
			#print number_favorite
			try:
				imageUrl=l.find_element_by_css_selector('div.is-preview img').get_attribute("src")
			except NoSuchElementException:
				imageUrl='none'

			#line='Post '+str(i)+' : username: '+username+' ; url: '+profile_url+' ; tweet: '+tweet_text+' ; '+date+' ; nb tweet:'+number_retweet+' ; nb_fav: '+number_favorite+' ; '
			#print line
			i=i+1
			print "url="+url_post
			print "profile="+profile_url
			curPost= post.Post('twitter',imageUrl,tweet_text,date,username,url_post,number_favorite,0,number_retweet,profile_url)
			list_post["posts"].append(curPost.getJSON())
		#print(json.dumps(list_post))
		return list_post
	except NoSuchElementException,e:
		print 'Error in getDetail of '+key+' :'
		print(traceback.format_exc())
		return 0
	except TimeoutException,e:
		print 'Time out for '+url+' :'
		return 0

def getAccount(key):
	try:
		print "Twitter: Getting users about "+key
		url='https://twitter.com/search?q='+key+'&src=typd&vertical=default&f=users'
		scroll(url)
		driver.wait = WebDriverWait(driver, 15)

		blogContents=driver.find_elements_by_css_selector('div.ProfileCard ')
		links=[]

		list_users={
			'users' :[]
		}
		for l in blogContents:
			user_id=l.get_attribute("data-user-id")
			link=getElementAttr('a.ProfileCard-bg',"href",l)
			if link != "-1":
				print user_id+" :"+link
				links.append(link)

		print 'Brownsing links now'

		for x in links:
			curUser=getProfileInfo(x)
			if curUser != 0:
				list_users["users"].append(curUser.getJSON())

		print 'Displaying result'
		#print json.dumps(list_users)
		return list_users
	except NoSuchElementException,e:
		print 'Error in getDetail of '+key+' :'
		print(traceback.format_exc())
		return 0
	except TimeoutException,e:
		print 'Time out for '+url+' :'
		return 

def login(url):
	driver.get(url)

	box = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".email-input")))
	try:
		username=driver.find_elements_by_css_selector(".email-input")[1]
		username.send_keys('djisse@gmail.com')
	except:
		print "Error cannot find username"
		print(traceback.format_exc())
		return -1

	try:
		password= driver.find_elements_by_css_selector('.js-password-field')[1]
		password.send_keys('paela95')
	except:
		print "Error cannot find password field"
		print(traceback.format_exc())
		return -1
	try:
		bt=driver.find_elements_by_css_selector('.submit')[1]
		bt.click()
	except:
		print "Error cannot find button for connexion"
		print(traceback.format_exc())
		return -1
	try:
		box = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.ProfileHeaderCard-nameLink")))
	except:
		print "Mauvaise redirection!"
		print(traceback.format_exc())
		return -1
	return 0

	#try:
	#	bt=driver.find_element_by_css_selector('')

def getFollowers(url):
	try:
		print "Twitter: Getting users of one page"
		
		ret=login(url)
		if ret==-1:
			print "Eror in connexion!"
			return -1
		scroll(url)
		
		blogContents=driver.find_elements_by_css_selector('div.ProfileCard ')
		links=[]

		list_users={
			'users' :[]
		}
		for l in blogContents:
			user_id=l.get_attribute("data-user-id")
			link=getElementAttr('a.ProfileCard-bg',"href",l)
			if link != "-1":
				print user_id+" :"+link
				links.append(link)

		print 'Brownsing links now'

		for x in links:
			curUser=getFollowing(x)
			if curUser != 0:
				list_users["users"].append(curUser)

		print 'Displaying result'
		print json.dumps(list_users)
		return list_users
	except NoSuchElementException,e:
		print 'Error in getDetail of '+key+' :'
		print(traceback.format_exc())
		return 0
	except TimeoutException,e:
		print 'Time out for '+url+' :'
		return 0



def getFollowing(url):
	try:
		print "Twitter: Getting followings "+url
		url=url+'/followers'
		driver.get(url)
		driver.wait = WebDriverWait(driver, 15)

		box = driver.wait.until(EC.presence_of_element_located((By.ID, "doc")))

		try:
			blogContents=driver.find_elements_by_css_selector('div.ProfileCard ')
		except NoSuchElementException:
			print "Error no user found!"
			return -1

		links=[]

		list_users={
			'users' :[]
		}
		print "This memeber is following: "
		for l in blogContents:
			user_id=l.get_attribute("data-user-id")
			link=getElementAttr('a.ProfileCard-bg',"href",l)
			if link != "-1":
				print user_id+" :"+link
				links.append(link)

		print 'Finish!'
		return links
	except:
		print "Error in getting following"
		return -1

def getProfileInfo(url):
	try:
		print "Twitter: Getting data a this user "+url
		driver.get(url)
		driver.wait = WebDriverWait(driver, 15)

		box = driver.wait.until(EC.presence_of_element_located((By.ID, "doc")))

		try:
			twitter_name=driver.find_element_by_css_selector(".ProfileCardMini-screenname span").get_attribute("textContent")
		except NoSuchElementException:
			twitter_name='none'
		try:
			twitter_img=driver.find_element_by_class_name("ProfileAvatar-image ").get_attribute("src")
		except NoSuchElementException:
			twitter_img='none'
		try:
			tweet= driver.find_element_by_css_selector("li.ProfileNav-item--tweets span.ProfileNav-value").get_attribute("textContent")
			tweet=utils.cleanNumber(tweet)
		except NoSuchElementException:
			tweet='none'
		try:
			following=driver.find_element_by_css_selector('li.ProfileNav-item--following span.ProfileNav-value').get_attribute("textContent")
			following=utils.cleanNumber(following)
		except NoSuchElementException:
			following='0'
		try:
			followers=driver.find_element_by_css_selector('li.ProfileNav-item--followers span.ProfileNav-value').get_attribute("textContent")
			followers=utils.cleanNumber(followers)
		except NoSuchElementException:
			followers='0'
		try:
			favorite=driver.find_element_by_css_selector('.ProfileNav-item--favorites a span.ProfileNav-value').get_attribute('textContent')
			favorite=utils.cleanNumber(favorite)
		except NoSuchElementException:
			favorite='0'
		try:
			url_avatar=driver.find_element_by_css_selector('.ProfileAvatar-image').get_attribute('src')
		except NoSuchElementException:
			url_avatar='none'
		try:
			location=driver.find_element_by_css_selector('.ProfileHeaderCard-locationText').get_attribute('textContent')
		except NoSuchElementException:
			location='none'
		try:
			url_web=driver.find_element_by_css_selector('.ProfileHeaderCard-urlText.u-dir a').get_attribute('textContent')
		except NoSuchElementException:
			url_web='none'
		#print twitter_name+": "+twitter_img+': '+tweet+': '+following+': '+followers+': '+favorite+'\n'
		
		curUser=user.User('twitter',twitter_name,location,url_avatar,followers,following,tweet,favorite,url_web,url)
		#print json.dumps(curUser.getJSON())

		return curUser
	except NoSuchElementException,e:
		print 'Error in getDetail of '+url+' :'
		print(traceback.format_exc())
		return 0
	except TimeoutException,e:
		print 'Time out for '+url+' :'
		return 0

def getImageinfo(key):
	try:
		print "Twitter: Getting list of image about"+ key
		url='https://twitter.com/search?q='+key+'&src=typd&vertical=default&f=images'
		scroll(url)
		driver.wait = WebDriverWait(driver, 15)

		links=[]

		tweet_urls=driver.find_elements_by_class_name("AdaptiveStreamGridImage")
		for l in tweet_urls:
			user_id=l.get_attribute("data-user-id")
			tweet_url=l.get_attribute("data-permalink-path")
			tweet_url="https://twitter.com"+tweet_url
			print user_id+' :'+tweet_url
			links.append(tweet_url)

		list_post={
			'post_img' :[]
		}
		for x in links:
			myPost=getdetail(x)
			list_post["post_img"].append(myPost.getJSON())

		print(json.dumps(list_post))
		return list_post
	except NoSuchElementException,e:
		print 'Error in getDetail of '+key+' :'
		print(traceback.format_exc())
		return 0
	except TimeoutException,e:
		print 'Time out for '+url+' :'
		return 0

def getdetail(url):
	try:
		print "Twitter: Getting details about this post: "+url
		driver.get(url)
		driver.wait = WebDriverWait(driver, 15)
		box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".js-tweet-text.tweet-text")))
		driver.wait = WebDriverWait(driver, 15)

		tweet_text=getElementAttr('.TweetTextSize','textContent',driver)
		tweet_text=re.sub(r'pic.twitter.com.*', " ", tweet_text)
		username=getElementAttr('.permalink-header .username b','textContent',driver)
		username=re.sub(r'Verified account', " ", username)
		profile_link="https://twitter.com/"+username
		try:
			retweet=driver.find_element_by_css_selector('a.request-retweeted-popup strong').get_attribute('textContent')
			retweet=utils.cleanNumber(retweet)
		except NoSuchElementException,e:
			retweet='0'
		try:
			favorite=driver.find_element_by_css_selector('a.request-favorited-popup strong').get_attribute('textContent')
			favorite=utils.cleanNumber(favorite)
		except NoSuchElementException,e:
			favorite='0'

		date=getElementAttr('span.metadata span','textContent',driver)
		try:
			img_url=driver.find_element_by_css_selector('.cards-media-container.js-media-container img').get_attribute("src")
		except NoSuchElementException,e:
			img_url='none'
		curPost= post.Post('twitter',img_url,tweet_text,date,username,url,favorite,0,retweet,profile_link)
		return curPost
		#print tweet_text+'\nUsername: '+username+'\nRetweet:'+retweet+'\nfavorite: '+favorite+'\nDate:'+date+'\nimageUrl:'+img_url
	except NoSuchElementException,e:
		print 'Error in getDetail of '+url+' :'
		print(traceback.format_exc())
		return 0
	except TimeoutException,e:
		print 'Time out for '+url+' :'
		return 0

def close():
	driver.close()