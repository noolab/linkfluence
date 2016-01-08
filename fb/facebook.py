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
import urllib
import friend
import json
reload(sys)
sys.setdefaultencoding("UTF8")
#browser=webdriver.Firefox()
profile_url=' '


path_to_chromedriver = '/Users/djisse/Documents/cheerio/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
def login(url):
	try:
		browser.get("https://www.facebook.fr/")
		try:
			box3 = browser.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fbxWelcomeBoxName")))
			browser.get(url)
			print "Already connected!"
			return 1
		except:
			print "Connection to facebook.com"

		browser.wait = WebDriverWait(browser, 15)
		
		box = browser.wait.until(EC.presence_of_element_located((By.NAME, "firstname")))
		firstname=browser.find_element_by_css_selector("form#login_form input#email")
		firstname.send_keys("aloylop@yahoo.com");
		email=browser.find_element_by_css_selector("form#login_form input#pass")
		email.send_keys("dara2015")
		try:
			submit=browser.find_elements_by_tag_name('input')[3]
			submit.click()
		except NoSuchElementException:
			print "not found"
			return -1
		
		try:
			box2 = browser.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fbxWelcomeBoxName")))
		except NoSuchElementException:
			return -1
			print "page not loaded after login"

		browser.get(url)
		return 1
	except NoSuchElementException:
		print 'Error in login'
		return -1

def getfriends(url):

	try:
		if login(url) ==-1:
			print 'Error in login'
			return -1
		username=url.split('/')[3]
		username=username.split('?')[0]
		list_friends={
			'username': username,
			'friends' :[]
		}

		try: 
			box1 = browser.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#fbTimelineHeadline div._70k")))
		except NoSuchElementException:
			print "Problem in loaing the good page" 
			return -1
		try:
			browser.find_element_by_css_selector('div#fbTimelineHeadline div._70k a:nth-child(3)').click()
			box = browser.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._3i9")))
		except NoSuchElementException:
			print 'Cannot process this page!'
			return -1
		for i in range(20):
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(1)

		try:
			allfriends=browser.find_elements_by_css_selector('div#pagelet_timeline_medley_friends li._698')
			for f in allfriends:
				try:
					name=f.find_element_by_css_selector('div.fsl.fwb.fcb a').get_attribute('textContent')
				except NoSuchElementException:
					name="no name"
				try:
					url_fr=f.find_element_by_css_selector('div._5qo4 a._5q6s').get_attribute('href')	
				except NoSuchElementException:
					url_fr="no profile"
				try:
					url_avatar=f.find_element_by_css_selector('div._5qo4 a._5q6s img').get_attribute('src')
				except NoSuchElementException:
					url_avatar="No url_avatar"
				curFriend=friend.Friend(name,url_fr,url_avatar)
				#print json.dumps(curFriend.getJSON())
				list_friends["friends"].append(curFriend.getJSON())

			return list_friends
		except NoSuchElementException:
			print "No list friend "
			return -1
	except NoSuchElementException:
		print "cannot open url friends tab"
		return -1
	except TimeoutException:
		print "Time out! Problem of connexion..."
		return -1

def getPageUserLike():
	#profile_url=browser.find_element_by_css_selector('div.rfloat._ohf li._4fn6._3zm- a').get_attribute("href")
	if "profile.php?id" in profile_url:
		print "match url "
		userLike=profile_url+'&sk=likes'
		browser.get(userLike)
		for i in range(5):
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
		try:
			allpage=browser.find_elements_by_css_selector('div#collection_wrapper_2409997254 div.fsl.fwb.fcb  a')
			for l in allpage:
				pagename=l.get_attribute("textContent")
				pageUrl=l.get_attribute('href')
				print pagename.encode('utf-8')
				print pageUrl
		except NoSuchElementException:
			print"No page like in this account"

	else:
		print "not match"
		userLike=profile_url+"/likes"
		browser.get(userLike)
		for i in range(5):
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
		try:
			allpage=browser.find_elements_by_css_selector('div#collection_wrapper_2409997254 div.fsl.fwb.fcb  a')
			for l in allpage:
				pagename=l.get_attribute("textContent")
				pageUrl=l.get_attribute('href')
				print pagename.encode('utf-8')
				print pageUrl
		except NoSuchElementException:
			print"No page like in this account"
		
	##getPageUserLike()
def getGroup():
	#profile_url=browser.find_element_by_css_selector('div.rfloat._ohf li._4fn6._3zm- a').get_attribute("href")
	if "profile.php?id" in profile_url:
		print "match url "
		userGroup=profile_url+'&sk=groups'
		browser.get(userGroup)
		for i in range(5):
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
		try:
			allpage=browser.find_elements_by_css_selector('div#collection_wrapper_2361831622 ul.uiList li div.mbs.fwb a:last-child')
			for l in allpage:
				groupname=l.get_attribute("textContent")
				groupUrl=l.get_attribute('href')
				groupUrl='https://www.facebook.com'+groupUrl
				print groupname.encode('utf-8')
				print groupUrl
		except NoSuchElementException:
			print"No Group in this account"
	else:
		print "not match"
		userGroup=profile_url+"/groups"
		browser.get(userGroup)
		for i in range(5):
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
		try:
			allpage=browser.find_elements_by_css_selector('div#collection_wrapper_2361831622 ul.uiList li div.mbs.fwb a:last-child')
			for l in allpage:
				groupname=l.get_attribute("textContent")
				groupUrl=l.get_attribute('href')
				groupUrl='https://www.facebook.com'+groupUrl
				print groupname.encode('utf-8')
				print groupUrl
		except NoSuchElementException:
			print"No Group in this account"
def getPlace():
	# profile_url=browser.find_element_by_css_selector('div.rfloat._ohf li._4fn6._3zm- a').get_attribute("href")
	if "profile.php?id" in profile_url:
		print "match url "
		usermap=profile_url+'&sk=map'
		# body = browser.find_element_by_tag_name("body")
		# body.send_keys(Keys.CONTROL + 't')
		browser.get(usermap)
		#browser.get('https://www.facebook.com/c.crave1/map')
		#time.sleep(2)
		try:
			allplace=browser.find_elements_by_css_selector('a._4o52 span._3sz')
			#print "allplace"+str(allplace)
			if len(allplace) > 0:
				for l in allplace:
					#print "get place name"
					placename=l.get_attribute("textContent")
					print placename.encode('utf-8')
			else:
				print "No place was check-In in this account"

		except NoSuchElementException:
			print "No place was check-In in this account"

	else:
		print "not match"
		usermap=profile_url+"/map"
		# body = browser.find_element_by_tag_name("body")
		# body.send_keys(Keys.CONTROL + 't')
		browser.get(usermap)
		time.sleep(2)
		try:
			allplace=browser.find_elements_by_css_selector('a._4o52 span._3sz')
			#print "allplace"+str(allplace)
			if len(allplace) > 0:
				for l in allplace:
					#print "get place name"
					placename=l.get_attribute("textContent")
					print placename.encode('utf-8')
			else:
				print "No place was check-In in this account"

		except NoSuchElementException:
			print "No place was check-In in this account"
def getPlaceVisit():
	#profile_url=browser.find_element_by_css_selector('div.rfloat._ohf li._4fn6._3zm- a').get_attribute("href")
	print "profile_url "+profile_url
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		userVisit=profile_url+'&sk=places_visited'
		print 'userVisit: '+userVisit
		try:
			body = browser.find_element_by_tag_name("body")
			#body.send_keys(Keys.CONTROL + 't')
			browser.get(userVisit)
			try:
				browser.wait = WebDriverWait(browser, 10)
				placeVisit=browser.find_elements_by_css_selector('div._gx6._agv a')
				for d in placeVisit:
					placeName=d.get_attribute('title')
					place_url=d.get_attribute('href')
					print placeName.encode('utf-8')
					print place_url
			except NoSuchElementException:
				print "No place visited"
		except NoSuchElementException:
			print "cannot open new tab"
	else:
		print "This url is not generate by fb>>>"
		userVisit=profile_url+"/places_visited"
		print 'userVisit: '+userVisit
		try:
			body = browser.find_element_by_tag_name("body")
			#body.send_keys(Keys.CONTROL + 't')
			browser.get(userVisit)
			try:
				browser.wait = WebDriverWait(browser, 10)
				placeVisit=browser.find_elements_by_css_selector('div._gx6._agv a')
				#print  'palce visit '+str(placeVisit)
				for d in placeVisit:
					placeName=d.get_attribute('title')
					place_url=d.get_attribute('href')
					print placeName.encode('utf-8')
					print place_url
			except NoSuchElementException:
				print ""
		except NoSuchElementException:
			print "cannot open new tab"
def getSport():
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		usersport=profile_url+'&sk=sports'
		print 'usersport: '+usersport
		try:
			browser.get(usersport)
			try:
				browser.wait = WebDriverWait(browser, 10)
				allSport=browser.find_elements_by_css_selector('div#collection_wrapper_330076653784935 div._gx6 a._gx7')
				for d in allSport:
					sportName=d.get_attribute('title')
					sport_url=d.get_attribute('href')
					print sportName.encode('utf-8')
					print sport_url
			except NoSuchElementException:
				print "No sport like"
		except NoSuchElementException:
			print "cannot open new url"
	else:
		print "This url is not generate by fb>>>"
		userVisit=profile_url+"/sports"
		try:
			browser.get(usersport)
			try:
				browser.wait = WebDriverWait(browser, 10)
				allSport=browser.find_elements_by_css_selector('div#collection_wrapper_330076653784935 div._gx6 a._gx7')
				for d in allSport:
					sportName=d.get_attribute('title')
					sport_url=d.get_attribute('href')
					print sportName.encode('utf-8')
					print sport_url
			except NoSuchElementException:
				print "No sport like"
		except NoSuchElementException:
			print "cannot open new url"
def getMovie():
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		userMovie=profile_url+'&sk=movies'
		try:
			browser.get(userMovie)
			try:
				browser.wait = WebDriverWait(browser, 10)
				allMovie=browser.find_elements_by_css_selector('div#collection_wrapper_177822289030932 div._gx6 a._gx7')
				for d in allMovie:
					movieName=d.get_attribute('title')
					movie_url=d.get_attribute('href')
					print movieName.encode('utf-8')
					print movie_url
			except NoSuchElementException:
				print "No sport like"
		except NoSuchElementException:
			print "cannot open new url"
	else:
		print "This url is not generate by fb>>>"
		userMovie=profile_url+"/movies"
		try:
			browser.get(userMovie)
			try:
				browser.wait = WebDriverWait(browser, 10)
				allMovie=browser.find_elements_by_css_selector('div#collection_wrapper_177822289030932 div._gx6 a._gx7')
				for d in allMovie:
					movieName=d.get_attribute('title')
					movie_url=d.get_attribute('href')
					print movieName.encode('utf-8')
					print movie_url
			except NoSuchElementException:
				print "No sport like"
		except NoSuchElementException:
			print "cannot open new url"
def getTV():
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		userTV=profile_url+'&sk=tv'
		try:
			browser.get(userTV)
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				browser.wait = WebDriverWait(browser, 10)
				allTV=browser.find_elements_by_css_selector('div#collection_wrapper_309918815775486 div._gx6 a._gx7 ')
				for d in allTV:
					tvName=d.get_attribute('title')
					tv_url=d.get_attribute('href')
					print tvName.encode('utf-8')
					print tv_url
			except NoSuchElementException:
				print "No TV like"
		except NoSuchElementException:
			print "cannot open new url"
	else:
		print "This url is not generate by fb>>>"
		userTV=profile_url+"/tv"
		try:
			browser.get(userTV)
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				browser.wait = WebDriverWait(browser, 10)
				allTV=browser.find_elements_by_css_selector('div#collection_wrapper_309918815775486 div._gx6 a._gx7 ')
				for d in allTV:
					tvName=d.get_attribute('title')
					tv_url=d.get_attribute('href')
					print movieName.encode('utf-8')
					print tv_url
			except NoSuchElementException:
				print "No TV like"
		except NoSuchElementException:
			print "cannot open new url"
def getBook():
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		userBook=profile_url+'&sk=books'
		try:
			browser.get(userBook)
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				browser.wait = WebDriverWait(browser, 10)
				allBook=browser.find_elements_by_css_selector('div#collection_wrapper_332953846789204 div._gx6 a._gx7')
				for d in allBook:
					bookName=d.get_attribute('title')
					book_url=d.get_attribute('href')
					print bookName.encode('utf-8')
					print book_url
			except NoSuchElementException:
				print "No Book like"
		except NoSuchElementException:
			print "cannot open new url"
	else:
		print "This url is not generate by fb>>>"
		userBook=profile_url+"/books"
		try:
			browser.get(userBook)
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				browser.wait = WebDriverWait(browser, 10)
				allBook=browser.find_elements_by_css_selector('div#collection_wrapper_332953846789204 div._gx6 a._gx7')
				for d in allBook:
					bookName=d.get_attribute('title')
					book_url=d.get_attribute('href')
					print bookName.encode('utf-8')
					print book_url
			except NoSuchElementException:
				print "No Book like"
		except NoSuchElementException:
			print "cannot open new url"
def getEvent():
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		userEvent=profile_url+'&sk=events'
		try:
			browser.get(userEvent)
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				browser.wait = WebDriverWait(browser, 10)
				allEvent=browser.find_elements_by_css_selector('div#collection_wrapper_2344061033  a._4cbt')
				for d in allEvent:
					eventName=d.get_attribute('textContent')
					event_url=d.get_attribute('href')
					print eventName.encode('utf-8')
					print event_url
			except NoSuchElementException:
				print "No events in this account"
		except NoSuchElementException:
			print "cannot open new url"
	else:
		print "This url is not generate by fb>>>"
		userEvent=profile_url+"/events"
		try:
			browser.get(userEvent)
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				browser.wait = WebDriverWait(browser, 10)
				allEvent=browser.find_elements_by_css_selector('div#collection_wrapper_2344061033  a._4cbt')
				for d in allEvent:
					eventName=d.get_attribute('textContent')
					event_url=d.get_attribute('href')
					print eventName.encode('utf-8')
					print event_url
			except NoSuchElementException:
				print "No events in this account"
		except NoSuchElementException:
			print "cannot open new url"
def getMusic():
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		userMusic=profile_url+'&sk=music'
		try:
			browser.get(userMusic)
			time.sleep(2)
			for i in range(5):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				browser.wait = WebDriverWait(browser, 10)
				allMusic=browser.find_elements_by_css_selector('div#collection_wrapper_221226937919712 div._gx6 a._gx7')
				for d in allMusic:
					musicName=d.get_attribute('textContent')
					music_url=d.get_attribute('href')
					print musicName.encode('utf-8')
					print music_url
			except NoSuchElementException:
				print "No events in this account"
		except NoSuchElementException:
			print "cannot open new url"
	else:
		print "This url is not generate by fb>>>"
		userMusic=profile_url+"/music"
		try:
			browser.get(userMusic)
			time.sleep(2)
			for i in range(5):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				browser.wait = WebDriverWait(browser, 10)
				allMusic=browser.find_elements_by_css_selector('div#collection_wrapper_221226937919712 div._gx6 a._gx7')
				for d in allMusic:
					musicName=d.get_attribute('textContent')
					music_url=d.get_attribute('href')
					print musicName.encode('utf-8')
					print music_url
			except NoSuchElementException:
				print "No events in this account"
		except NoSuchElementException:
			print "cannot open new url"
def getVideo():
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		userVideo=profile_url+'&sk=videos'
		try:
			browser.get(userVideo)
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				allVideo=browser.find_elements_by_css_selector('div#collection_wrapper_1560653304174514 a')
				for d in allVideo:
					video_url=d.get_attribute('href')
					print video_url
			except NoSuchElementException:
				print "No video in this account"
		except NoSuchElementException:
			print "cannot open new url"
	else:
		print "This url is not generate by fb>>>"
		userVideo=profile_url+"/videos"
		try:
			browser.get(userVideo)
			#browser.get('https://www.facebook.com/sa.mok.5667/videos')
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				allVideo=browser.find_elements_by_css_selector('div#collection_wrapper_1560653304174514 a')
				for d in allVideo:
					video_url=d.get_attribute('href')
					print video_url
			except NoSuchElementException:
				print "No video in this account"
		except NoSuchElementException:
			print "cannot open new url"
def getAppGame():
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		userAppGame=profile_url+'&sk=games'
		try:
			browser.get(userAppGame)
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				allAppGame=browser.find_elements_by_css_selector('div#collection_wrapper_249944898349166 div._gx6 a._gx7')
				for d in allAppGame:
					nameAppGame=d.get_attribute('title')
					appGame_url=d.get_attribute('href')
					print nameAppGame
					print appGame_url
			except NoSuchElementException:
				print "No Game or App in this account"
		except NoSuchElementException:
			print "cannot open new url"
	else:
		print "This url is not generate by fb>>>"
		userAppGame=profile_url+"/games"
		try:
			browser.get(userAppGame)
			#browser.get('https://www.facebook.com/sa.mok.5667/videos')
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				allAppGame=browser.find_elements_by_css_selector('div#collection_wrapper_249944898349166 div._gx6 a._gx7')
				for d in allAppGame:
					nameAppGame=d.get_attribute('title')
					appGame_url=d.get_attribute('href')
					print nameAppGame
					print appGame_url
			except NoSuchElementException:
				print "No Game or App in this account"
		except NoSuchElementException:
			print "cannot open new url"
def getNotes():
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		userNote=profile_url+'&sk=notes'
		try:
			browser.get(userNote)
			#browser.get('https://www.facebook.com/sokheng.hedc/notes')
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				allNote=browser.find_elements_by_css_selector('div.userContentWrapper')
				for d in allNote:
					noteTitle=d.find_element_by_css_selector('div._4_j6 div._4_j7 a').get_attribute('textContent')
					note_url=d.find_element_by_css_selector('div._4_j6 div._4_j7 a').get_attribute('href')
					noteText=d.find_element_by_tag_name('p').get_attribute('textContent')
					print noteTitle.encode('utf-8')
					print note_url
					print noteText.encode('utf-8')
			except NoSuchElementException:
				print "No Notes in this account"
		except NoSuchElementException:
			print "cannot open new url"
	else:
		print "This url is not generate by fb>>>"
		userNote=profile_url+"/notes"
		try:
			browser.get(userNote)
			#browser.get('https://www.facebook.com/sa.mok.5667/videos')
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				allNote=browser.find_elements_by_css_selector('div.userContentWrapper')
				for d in allNote:
					noteTitle=d.find_element_by_css_selector('div._4_j6 div._4_j7 a').get_attribute('textContent')
					note_url=d.find_element_by_css_selector('div._4_j6 div._4_j7 a').get_attribute('href')
					noteText=d.find_element_by_tag_name('p')
					print noteTitle.encode('utf-8')
					print note_url
					print noteText.encode('utf-8')
			except NoSuchElementException:
				print "No Notes in this account"
		except NoSuchElementException:
			print "cannot open new url"
def getReview():
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		userReview=profile_url+'&sk=reviews'
		try:
			browser.get(userReview)
			#browser.get('https://www.facebook.com/Pen.Bopha/reviews')
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				allReview=browser.find_elements_by_css_selector('div#collection_wrapper_254984101287276 span.fwb a')
				for d in allReview:
					reviewName=d.get_attribute('textContent')
					review_url=d.get_attribute('href')
					print reviewName.encode('utf-8')
					print review_url
			except NoSuchElementException:
				print "No reviews in this account"
		except NoSuchElementException:
			print "cannot open new url"
	else:
		print "This url is not generate by fb>>>"
		userReview=profile_url+"/reviews"
		try:
			browser.get(userReview)
			#browser.get('https://www.facebook.com/sa.mok.5667/videos')
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				allReview=browser.find_elements_by_css_selector('div#collection_wrapper_254984101287276 span.fwb a')
				for d in allReview:
					reviewName=d.get_attribute('textContent')
					review_url=d.get_attribute('href')
					print reviewName.encode('utf-8')
					print review_url
			except NoSuchElementException:
				print "No reviews in this account"
		except NoSuchElementException:
			print "cannot open new url"
def getWork_edu():
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		userWork_edu=profile_url+'&sk=about&section=education&pnref=about'
		try:
			browser.get(userWork_edu)
			##browser.get('https://www.facebook.com/sokheng.hedc/about?section=education&pnref=about')
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				allWork_edu=browser.find_elements_by_css_selector('div._4qm1')
				for d in allWork_edu:
					try:
						categoryName=d.find_element_by_css_selector('span._h72 ').get_attribute('textContent')
						print categoryName.encode('utf-8')
					except NoSuchElementException:
						print "category of wwork and education not found"
					try:
						titles=d.find_elements_by_css_selector('li.fbEditProfileViewExperience ')
						for l in titles:
							#get name of edu and workplace 
							try:
								name=l.find_element_by_css_selector('div._42ef a').get_attribute('textContent')
								name_url=l.find_element_by_css_selector('div._42ef a').get_attribute('href')
							except NoSuchElementException:
								print "element not ffound"
							try:
								date=l.find_element_by_css_selector('div.fsm').get_attribute('textContent')
							except NoSuchElementException:
								print 'no date '
							print 'name is: '+name.encode('utf-8')
							print 'date is:' +date.encode('utf-8')
						# title=d.find_element_by_css_selector('div._4qm1 div._6a._6b:last-child').get_attribute('textContent')
						# print  title.encode('utf-8')

					except NoSuchElementException:
						print "no work and education"
					
			except NoSuchElementException:
				print "Element of work and education is not found"
		except NoSuchElementException:
			print "cannot open new url"
	else:
		print "This url is not generate by fb>>>"
		userWork_edu=profile_url+"/about?section=education&pnref=about"
		try:
			browser.get(userWork_edu)
			#browser.get('https://www.facebook.com/sa.mok.5667/videos')
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				allWork_edu=browser.find_elements_by_css_selector('div._4qm1')
				for d in allWork_edu:
					try:
						categoryName=d.find_element_by_css_selector('span._h72 ').get_attribute('textContent')
						print categoryName.encode('utf-8')
					except NoSuchElementException:
						print "category of wwork and education not found"
					try:
						titles=d.find_elements_by_css_selector('li.fbEditProfileViewExperience ')
						for l in titles:
							#get name of edu and workplace 
							try:
								name=l.find_element_by_css_selector('div._42ef a').get_attribute('textContent')
								name_url=l.find_element_by_css_selector('div._42ef a').get_attribute('href')
							except NoSuchElementException:
								print "element not ffound"
							try:
								date=l.find_element_by_css_selector('div.fsm').get_attribute('textContent')
							except NoSuchElementException:
								print 'no date '
							print 'name is: '+name.encode('utf-8')
							print date.encode('utf-8')
						# title=d.find_element_by_css_selector('div._4qm1 div._6a._6b:last-child').get_attribute('textContent')
						# print  title.encode('utf-8')
					except NoSuchElementException:
						print "no work and education"
					
			except NoSuchElementException:
				print "Element of work and education is not found"
		except NoSuchElementException:
			print "cannot open new url"
def getPlaceUserLive():
	if "profile.php?id" in profile_url:
		print "The url is generate by fb>>>"
		userPlace_live=profile_url+'&sk=about&section=living&pnref=about'
		try:
			browser.get(userPlace_live)
			##browser.get('https://www.facebook.com/sokheng.hedc/about?section=education&pnref=about')
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				allWork_edu=browser.find_elements_by_css_selector('div._4qm1')
				for d in allWork_edu:
					try:
						categoryName=d.find_element_by_css_selector('span._h72 ').get_attribute('textContent')
						print categoryName.encode('utf-8')
					except NoSuchElementException:
						print "category of place living not found"
					try:
						currentPlace=d.find_element_by_css_selector('li#current_city div._6a._6b:last-child a ').get_attribute('textContent')
						print 'current place'+currentPlace
					except NoSuchElementException:
						print "no current place"
					try:
						hometownPlace=d.find_element_by_css_selector('li#hometown div._6a._6b:last-child a ').get_attribute('textContent')
						print 'hometownPlace '+hometownPlace
					except NoSuchElementException:
						print "no hometown place"
			except NoSuchElementException:
				print "Element of work and education is not found"
		except NoSuchElementException:
			print "cannot open new url"
	else:
		print "This url is not generate by fb>>>"
		userWork_edu=profile_url+"/about?section=education&pnref=about"
		try:
			browser.get(userWork_edu)
			#browser.get('https://www.facebook.com/sa.mok.5667/videos')
			time.sleep(2)
			for i in range(3):
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(2)
			try:
				allWork_edu=browser.find_elements_by_css_selector('div._4qm1')
				for d in allWork_edu:
					try:
						categoryName=d.find_element_by_css_selector('span._h72 ').get_attribute('textContent')
						print categoryName.encode('utf-8')
					except NoSuchElementException:
						print "category of wwork and education not found"
					try:
						titles=d.find_elements_by_css_selector('li.fbEditProfileViewExperience ')
						for l in titles:
							#get name of edu and workplace 
							try:
								name=l.find_element_by_css_selector('div._42ef a').get_attribute('textContent')
								name_url=l.find_element_by_css_selector('div._42ef a').get_attribute('href')
							except NoSuchElementException:
								print "element not ffound"
							try:
								date=l.find_element_by_css_selector('div.fsm').get_attribute('textContent')
							except NoSuchElementException:
								print 'no date '
							print 'name is: '+name.encode('utf-8')
							print date.encode('utf-8')
						# title=d.find_element_by_css_selector('div._4qm1 div._6a._6b:last-child').get_attribute('textContent')
						# print  title.encode('utf-8')
					except NoSuchElementException:
						print "no work and education"
					
			except NoSuchElementException:
				print "Element of work and education is not found"
		except NoSuchElementException:
			print "cannot open new url"

def extractFriend(url):
	username=url.split('/')[3]
	friends={'list':[]}
	friends['list'].append(getfriends(url))
	#print json.dumps(friends)
	return friends

def extractAllAfriends(url):
	myList=extractFriend(url)
	if myList==-1:
		return -1
	username=url.split('/')[3]
	amis=myList['list'][0]['friends']

	for ami in amis:
		print 'getting friends of '+ami['name']
		data=getfriends(ami['profile'])
		myList['list'].append(data)
		#print "adding: "
		#print json.dumps(data)
	fo = open("data.json", "rw+")
	line = fo.write(json.dumps(myList))
	#print json.dumps(myList)


def close():
	browser.close()


# txtEmail=sys.argv[1]
# txtPass=sys.argv[2]
# getfriends(txtEmail,txtPass)


extractAllAfriends('https://www.facebook.com/djidji.djisse')
close()
