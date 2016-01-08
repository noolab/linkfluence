import sys
import twitter
from selenium.common.exceptions import NoSuchElementException
import database
import json
import traceback


database.insta.driver.close()
database.facebook.driver.close()

key=sys.argv[1]

try:
	
	mypost=twitter.getPostInstant(key)
	if mypost !=0:
		print 'inserting post of this search:'+key
		database.insertPost(mypost)

	twitter.close()
except:
	print(traceback.format_exc())
	database.twitter.driver.close()
