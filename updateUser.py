import database
import json


def getMembers():
	return database.db.members.find()

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
			database.updateStatUser(curUser["link"],curUser["username"],curUser["website"],curUser["nb_followers"],curUser["nb_posts"],curUser["url_avatar"],curUser["nb_favorite"],curUser["nb_following"])

updateProfile()

database.facebook.driver.close()
database.twitter.driver.close()
database.insta.driver.close()