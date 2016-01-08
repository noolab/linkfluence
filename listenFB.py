import sys
import facebook
from selenium.common.exceptions import NoSuchElementException
import database
import json
import traceback

try:
	database.insta.driver.close()
	database.twitter.driver.close()
	key=sys.argv[1]


	mypost=facebook.login(key)

	if mypost !=0:
		print 'inserting post of this search:'+key
		database.insertPost(mypost)

	facebook.close()
except:
	print(traceback.format_exc())
	database.facebook.driver.close()


#database.getId("Nike")