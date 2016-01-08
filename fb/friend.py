import json

class Friend:

   def __init__(self,name,profile,avatar):
      self.name = name
      self.profile = profile
      self.avatar = avatar
   
   def getJSON(self):
     myJSON = {
         'name'          : self.name,
         'profile'         : self.profile,
         'avatar'         : self.avatar,
     }
     #print(json.dumps(myJSON))
     return myJSON


