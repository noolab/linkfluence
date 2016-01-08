import json

class User:

   def __init__(self,website,username,location,url_avatar,nb_followers,nb_following,nb_posts,nb_favorite,personnal_web,link):
      self.website = website
      self.username = username
      self.location = location
      self.url_avatar = url_avatar
      self.nb_followers = nb_followers
      self.nb_following = nb_following
      self.nb_posts = nb_posts
      self.nb_favorite=nb_favorite
      self.personnal_web=personnal_web
      self.link=link
   
   def getJSON(self):
     myJSON = {
         'website'          : self.website,
         'username'         : self.username,
         'location'         : self.location,
         'url_avatar'       : self.url_avatar,
         'nb_followers'     : self.nb_followers,
         'nb_following'     : self.nb_following,
         'nb_posts'         : self.nb_posts,
         'nb_favorite'      : self.nb_favorite,
         'personnal_web'    : self.personnal_web,
         'link'             : self.link

     }
     #print(json.dumps(myJSON))
     return myJSON


