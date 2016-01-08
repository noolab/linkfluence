from pymongo import MongoClient
import json
import sys
import twitter
import insta
import facebook
import utils
from bson.objectid import ObjectId
from aylienapiclient import textapi

mongolab_uri = "mongodb://localhost:3001/"

client = MongoClient(mongolab_uri,
                     connectTimeoutMS=10000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)
db = client.meteor

def updatePost(link,nb_comments,nb_share,nb_likes):
	stats={
		"link":link,
		"nb_comments":nb_comments,
		"nb_share": nb_share,
		"nb_likes":nb_likes
	}
	
	db.members.update({"posts.link": link},{ "$set": {
		"posts.$.link": link,
		"posts.$.nb_comments": nb_comments,
		"posts.$.nb_share": nb_share,
		"posts.$.nb_likes": nb_likes
	}})
	db.stats_posts.insert(stats)
	print "Post updated!"

def updateStatUser(profile,username,website,nb_followers,nb_posts,url_avatar,nb_favorite,nb_following):
	user=getUser(profile,website)
	statsMembers={
		"nb_followers":nb_followers,
		"nb_posts": nb_posts,
		"url_avatar":url_avatar,
		"nb_favorite":nb_favorite,
		"nb_following":nb_following
	}
	stats={
		"userId":user["_id"],
		"nb_followers":nb_followers,
		"nb_posts": nb_posts,
		"url_avatar":url_avatar,
		"nb_favorite":nb_favorite,
		"nb_following":nb_following
	}
	db.members.update({ "_id":ObjectId(user['_id'])},{"$set": statsMembers})
	db.stats_members.insert_one(stats)
	print "User Updated!"


def insertUser(data):
	try:
		print "inserting user"
		#list = json.load(data)
		monjson=data['users']
		for line in monjson:
			website = line['website']
			username = line['username']
			url_avatar = line['url_avatar']
			nb_followers = line['nb_followers']
			nb_following = line['nb_following']
			link = line['link']
			nb_posts = line['nb_posts']
			location = line['location']
			nb_favorite = line['nb_favorite']
			personnal_web = line['personnal_web']
			curid=getId(username)
			if curid ==-1 :
				print 'insert new member!'
				result = db.members.insert_one({
					 'website'          : website,
					 'username'         : username,
					 'location'         : location,
					 'url_avatar'       : url_avatar,
					 'nb_followers'     : nb_followers,
					 'nb_following'     : nb_following,
					 'nb_posts'         : nb_posts,
					 'nb_favorite'      : nb_favorite,
					 'personnal_web'    : personnal_web,
					 'link'    			: link,
					 'posts'			: []

				})
			else:
				result = db.members.update({'_id': curid},{ "$set":{
					 'website'          : website,
					 'username'         : username,
					 'location'         : location,
					 'url_avatar'       : url_avatar,
					 'nb_followers'     : nb_followers,
					 'nb_following'     : nb_following,
					 'nb_posts'         : nb_posts,
					 'nb_favorite'      : nb_favorite,
					 'link'      		: link,
					 'personnal_web'    : personnal_web

				}})
	except AttributeError,e:
		print "Error in reading JSOn file(insertUser): "
		print json.dumps(data)
		print e

def insertCommentInsta(link,username,text):
	print "verification..."
	verif=db.members.find({"posts.link":link,"posts.comments.username":username,"posts.comments.text":text})
	if verif.count()==0:
		polarity=utils.sentiment(text)
		print "inserting "+polarity
		db.members.update({"posts.link":link},{"$addToSet":{
				"posts.$.comments":{"username":username,"text":text,"polarity":polarity}
				}})
		print "post updated"

def insertCommentFB(link,username,text,date,avatar,profile):
	verif=db.members.find({"posts.link":link,"posts.comments.username":username,"posts.comments.text":text})
	if verif.count()==0:
		polarity=utils.sentiment(text)
		print "inserting "+polarity
		db.members.update({"posts.link":link},{"$addToSet":{
				"posts.$.comments":{"username":username,"text":text,"polarity":polarity,"date":date,"avatar":avatar,"profile":profile}
				}})

def insertCommentsInsta(link):
	listComments=insta.getComment(link)
	monjson=listComments['comments']
	for line in monjson:
		text=line["text"]
		username=line["username"]
		insertCommentInsta(link,username,text)

def insertCommentsFB(link):
	listComments=facebook.getComment(link)
	monjson=listComments['comments']
	for line in monjson:
		text=line["text"]
		username=line["username"]
		avatar=line["avatar"]
		profile=line["profile"]
		date=line["date"]
		insertCommentFB(link,username,text,date,avatar,profile)

def insertPost(data):
	print 'inserting post...'
	#list = json.load(data)
	try:
		monjson=data['posts']
		for line in monjson:
			website = line['website']
			url_image = line['url_image']
			text = line['text']
			date = line['date']
			author_username = line['author_username']
			link = line['link']
			nb_likes = line['nb_likes']
			nb_comments = line['nb_comments']
			profile = line['profile']
			nb_share = line['nb_share']
			
			mypost={
				'website'         : website,
				'url_image'       : url_image,
				'text'            : text,
				'date'            : date,
				'author_username' : author_username,
				'link'            : link,
				'nb_likes'        : nb_likes,
				'nb_comments'     : nb_comments,
				'profile'         : profile,
				'nb_share'        : nb_share
			}
			print "searching comment"
			upsertPost(mypost)
	except AttributeError,e:
		print "Error in reading JSOn file(insert Post)"
		print json.dumps(data)
		print e

def getId(username):
	users=db.members.find({"username":username})
	if users.count() >=1:
		user=users.next()
		print user["_id"]
		return user["_id"]
	else:
		return -1

def getUser(profile,website):
	users=db.members.find({"link":profile,"website":website})
	if users.count() >=1:
		user=users.next()
		return user
	else:
		profile=profile.replace('https','http')
		users=db.members.find({"link":profile,"website":website})
		if users.count() >=1:
			user=users.next()
			return user
		else:
			return -1

def upsertPost(post):
	print "upserting post"
	user=getUser(post["profile"],post["website"])
	if user !=-1 :
		print "User found for this post: "+user["username"] +" => "+post["link"]

		curpost=db.members.find({"posts.link":post["link"]})
		print "memebers found: "+str(curpost.count())
		if curpost.count() >0:
			db.members.update({"posts.link": post["link"]},{ "$set": {"posts.$": post} })
			print "post updated!"
		else:
			print "adding the post"
			try:
				newUser={
					 'website'          : user['website'],
					 'username'         : user['username'],
					 'location'         : user['location'],
					 'url_avatar'       : user['url_avatar'],
					 'nb_followers'     : user['nb_followers'],
					 'nb_following'     : user['nb_following'],
					 'nb_posts'         : user['nb_posts'],
					 'nb_favorite'      : user['nb_favorite'],
					 'personnal_web'    : user['personnal_web'],
					 'posts'			: [],
					 'link'    			: user['link']
				}
				for p in user["posts"]:
					website = p['website']
					url_image = p['url_image']
					text = p['text']
					date = p['date']
					author_username = p['author_username']
					link = p['link']
					nb_likes = p['nb_likes']
					nb_comments = p['nb_comments']
					profile = p['profile']
					nb_share = p['nb_share']
			
					mypost={
						'website'         : website,
						'url_image'       : url_image,
						'text'            : text,
						'date'            : date,
						'author_username' : author_username,
						'link'            : link,
						'nb_likes'        : nb_likes,
						'nb_comments'     : nb_comments,
						'profile'         : profile,
						'nb_share'        : nb_share
					}
					newUser["posts"].append(mypost)
				newUser["posts"].append(post)
				print "adding post"
			except KeyError:
				newUser=user
			result = db.members.update({"_id":ObjectId(user['_id'])},newUser)
			print "Post added:"
			#print json.dumps(user)
	else:
		print "No user found for this post... inserting "+post["profile"]+" / "+post["website"]
		if post["website"] == "twitter":
			insertUserByLink("http://twitter.com/"+post["author_username"])
		if post["website"] == "instagram":
			insertUserInsta(post["author_username"])
		if post["website"] == "facebook":
			print "inserting new user : "+post["profile"]
			insertUserFB(post["profile"])
		upsertPost(post)


def insertUserByLink(url):
	print "Inserting user by link "+url
	info=twitter.getProfileInfo(url)
	print json.dumps(info.getJSON())
	info=info.getJSON()
	if info !=0:
		list_users={
				'users' :[{
					 'website'          : info['website'],
					 'username'         : info['username'],
					 'location'         : info['location'],
					 'url_avatar'       : info['url_avatar'],
					 'nb_followers'     : info['nb_followers'],
					 'nb_following'     : info['nb_following'],
					 'nb_posts'         : info['nb_posts'],
					 'nb_favorite'      : info['nb_favorite'],
					 'personnal_web'    : info['personnal_web'],
					 'link'    : info['link']
				}]
		}
		insertUser(list_users)

def insertUserInsta(username):
	print "Inserting user insta "+username
	info=insta.getUser(username)
	#print json.dumps(info.getJSON())
	info=info.getJSON()
	if info !=0:
		list_users={
				'users' :[{
					 'website'          : info['website'],
					 'username'         : info['username'],
					 'location'         : info['location'],
					 'url_avatar'       : info['url_avatar'],
					 'nb_followers'     : info['nb_followers'],
					 'nb_following'     : info['nb_following'],
					 'nb_posts'         : info['nb_posts'],
					 'nb_favorite'      : info['nb_favorite'],
					 'personnal_web'    : info['personnal_web'],
					 'link'    			: info['link']
				}]
		}
		insertUser(list_users)

def insertUserFB(link):
	print "Inserting user fb "+link
	info=facebook.getUser(link)
	#print json.dumps(info.getJSON())
	info=info.getJSON()
	if info !=0:
		list_users={
				'users' :[{
					 'website'          : info['website'],
					 'username'         : info['username'],
					 'location'         : info['location'],
					 'url_avatar'       : info['url_avatar'],
					 'nb_followers'     : info['nb_followers'],
					 'nb_following'     : info['nb_following'],
					 'nb_posts'         : info['nb_posts'],
					 'nb_favorite'      : info['nb_favorite'],
					 'personnal_web'    : info['personnal_web'],
					 'posts'			: [],
					 'link'    			: info['link']
				}]
		}
		insertUser(list_users)
		print 'insertion finished!'
	else:
		print 'error in retriving data!'
