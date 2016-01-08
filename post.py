import json

class Post:

   def __init__(self,website,url_image,text,date,author_username,link,nb_likes,nb_comments,nb_share,profile):
      self.website = website
      self.url_image = url_image
      self.text = text
      self.date = date
      self.author_username = author_username
      self.link = link
      self.nb_likes = nb_likes
      self.nb_comments = nb_comments
      self.nb_share = nb_share
      self.profile = profile
   
   def getJSON(self):
     myJSON = {
         'website'         : self.website,
         'url_image'       : self.url_image,
         'text'            : self.text,
         'date'            : self.date,
         'author_username' : self.author_username,
         'link'            : self.link,
         'nb_likes'        : self.nb_likes,
         'nb_comments'     : self.nb_comments,
         'profile'         : self.profile,
         'nb_share'        : self.nb_share

     }
     return myJSON
