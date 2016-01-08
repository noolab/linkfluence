import utils
import sys
reload(sys)
sys.setdefaultencoding("UTF8")


chaine='35,9&nbsp;k'
chaine=chaine.replace(u'\xa0', ' ')
chaine=chaine.replace(u'\xc2', ' ')
print len(chaine.split(' '))
utils.cleanNumber(chaine)