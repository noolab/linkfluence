import json
import database
database.facebook.close()
database.twitter.close()
data=database.insertCommentsInsta("https://instagram.com/p/56uKDUI94j/?taken-by=safirstores")

database.insta.close()

#already have https://instagram.com/p/6AH8JgR5YY/?tagged=sisley