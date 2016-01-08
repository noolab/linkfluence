import sys
import twitter
from selenium.common.exceptions import NoSuchElementException
import database
import json


database.insta.driver.close()
database.facebook.driver.close()

key=sys.argv[1]

try:
	myJSON=twitter.getAccount(key)

	if myJSON !=0:
		print "insert user of this search"+key
		database.insertUser(myJSON)

	mypost=twitter.getPost(key)

	if mypost !=0:
		print 'inserting post of this search:'+key
		database.insertPost(mypost)

	twitter.close()
except:
	driver.close()


#database.getId("Nike")