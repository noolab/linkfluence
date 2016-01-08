import database
import json


def getMembers():
	return database.db.members.find()

def getPosts():
	posts=database.db.members.find({},{"posts": "true"})
	for pp in posts:
		if "posts" in pp:
			for p in pp["posts"]:
				curPost=0
				if p["website"]=='instagram':
					curPost=database.insta.getdetail(p["link"])
				if p["website"]=='twitter':
					curPost=database.twitter.getdetail(p["link"])
				if p["website"]=="facebook":
					curPost=-1
				if curPost !=0 and curPost !=-1:
					curPost=curPost.getJSON()
					print "searching comments..."
					database.updatePost(p["link"],p["nb_comments"],p["nb_share"],p["nb_likes"])
				if curPost ==0:
					print "Error for this post: "+p["link"]

try:
	getPosts()
except:
	print "Error"
finally:
	database.facebook.driver.close()
	database.twitter.driver.close()
	database.insta.driver.close()