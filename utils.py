from decimal import Decimal
import detectlanguage
from apiclient.discovery import build
import indicoio
detectlanguage.configuration.api_key = "ec8fee3835542300e5beba24fa64dfe9"
print "loading api"
service = build('translate', 'v2',developerKey='AIzaSyBtJHFXBJnFwmiykSRsFfxdCio9_5F_dRM')
indicoio.config.api_key = '80a6e5b8319ee2664ba0e5cc7a6f921d'
import sys
reload(sys)
sys.setdefaultencoding("UTF8")
def cleanNumber(txt):
	txt=str(txt)
	txt=txt.replace(u'\xa0', ' ')
	txt=txt.replace(u'\xc2', ' ')
	print "converting "+txt
	print len(txt.split(' '))
	result=0
	virgule=-1
	
	for s in txt.split( ):
		s=s.upper()

		s=s.replace(',','.')
		havecomma=len(str(s).split('.'))
		if havecomma>1:
			virgule=1
		try:
			result=float(s)
		except:
			if s.endswith('K'):
				if len(s)>1:
					print "processing "+s
					result=float(s[0:-1])*1000
				else:
					result=float(result)*1000
			if s.endswith('M'):
				if len(s)>1:
					result=float(s[0:-1])*1000000
				else:
					result=float(result)*1000000
	if virgule !=-1 and result<1000:
		result=result*1000
	result=round(result,2)
	print "result="+str(result)
	return result

def detectLanguage(txt):
	return detectlanguage.simple_detect(txt)


def detectLang(txt):
	try:
		#print "api loaded! translating..."
		result= service.detections().list(q=[txt]).execute()
		print "lang="+result["detections"][0][0]["language"]
		return result["detections"][0][0]["language"]
	except:
		return "en"

def translate(txt):
	try:
		#print "api loaded! translating..."
		src=detectLang(txt)
		result= service.translations().list(source=src,target='en',q=[txt]).execute()
		print txt+" = "+result["translations"][0]["translatedText"]
		return result["translations"][0]["translatedText"]
	except:
		return txt

def sentiment(txt):
	try:
		tmp=translate(txt)
		val=indicoio.sentiment(tmp)
		if val<0.7 and val>0.3:
			return 'neutral'
		if val<0.4:
			return 'negative'
		if val>0.7:
			return 'positive'
	except:
		return "none"

