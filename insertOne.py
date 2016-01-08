import sys
import twitter
from selenium.common.exceptions import NoSuchElementException
import database
import json

myJSON1=twitter.getProfileInfo("https://twitter.com/kaepora")

if myJSON1 !=0:
	myJSON=myJSON1.getJSON()
	print "insert user of this search"
	list_users={
				'users' :[{
					 'website'          : myJSON['website'],
					 'username'         : myJSON['username'],
					 'location'         : myJSON['location'],
					 'url_avatar'       : myJSON['url_avatar'],
					 'nb_followers'     : myJSON['nb_followers'],
					 'nb_following'     : myJSON['nb_following'],
					 'nb_posts'         : myJSON['nb_posts'],
					 'nb_favorite'      : myJSON['nb_favorite'],
					 'personnal_web'    : myJSON['personnal_web']
				}]
		}
	database.insertUser(list_users)

mypost=twitter.getdetail("https://twitter.com/michael_nielsen/status/627170086076481537")

if mypost !=0:
	print 'inserting post of this search:'
	monjson=mypost.getJSON()
	list_posts={
				'posts' :[{
			    'website'         : monjson["website"],
				'url_image'       : monjson["url_image"],
				'text'            : monjson["text"],
				'date'            : monjson["date"],
				'author_username' : monjson["author_username"],
				'link'            : monjson["link"],
				'nb_likes'        : monjson["nb_likes"],
				'nb_comments'     : monjson["nb_comments"],
				'nb_share'        : monjson["nb_share"]
				}]
		}
	database.insertPost(list_posts)

twitter.close()


#database.getId("Nike")