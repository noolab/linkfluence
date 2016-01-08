import sys
import insta
from selenium.common.exceptions import NoSuchElementException
import database
import json
import traceback

try:
	database.facebook.driver.close()
	database.twitter.driver.close()

	key=sys.argv[1]


	mypost=insta.getImgLink(key)

	if mypost !=0:
		print 'inserting post of this search:'+key
		database.insertPost(mypost)

	insta.close()
except:
	print(traceback.format_exc())
	database.insta.driver.close()


#database.getId("Nike")