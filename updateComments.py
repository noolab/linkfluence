import database
import json


def getComments():
	posts=database.db.members.find({},{"posts": "true"})
	for pp in posts:
		if "posts" in pp:
			for p in pp["posts"]:
				print "searching comments..."
				if p["website"]=='instagram':
					database.insertCommentsInsta(p["link"])
				if p["website"]=='facebook':
					database.insertCommentsFB(p["link"])

try:
	getComments()
except:
	print "Error"
finally:
	database.facebook.driver.close()
	database.twitter.driver.close()
	database.insta.driver.close()