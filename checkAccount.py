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
				if curPost !=0:
					curPost=curPost.getJSON()
					database.updatePost(p["link"],p["nb_comments"],p["nb_share"],p["nb_likes"])



def updateProfile():
	users=getMembers()

	for u in users:
		curUser=None
		if u["website"] =='instagram':
			curUser=database.insta.getUser(u["username"])
		if u["website"] =='facebook':
			curUser=database.facebook.getUser(u["link"])
		if u["website"] =='twitter':
			curUser=database.twitter.getProfileInfo(u["link"])
		if curUser != 0:
			print curUser.getJSON()
			curUser=curUser.getJSON()
			database.updateStatUser(curUser["username"],curUser["website"],curUser["nb_followers"],curUser["nb_posts"],curUser["url_avatar"],curUser["nb_favorite"],curUser["nb_following"])
