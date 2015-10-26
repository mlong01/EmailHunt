import sys
import re
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  

# Any num of non-whitespace chars followed by @ followed by a word
# followed by a '.' followed by another word
EMAIL_REGEX = '\S*@\w*.\w*'
NEW_REGEX = '(\w+(\.\w*)*@\w*(\.\w*)*)'

### This class taken from (url plug in later) ###
class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit() 
#################################################

if len(sys.argv) != 2:
    print "USAGE: python scrape.py [url]"
    sys.exit(0)

# Format so requests recognizes
url = "http://" + sys.argv[1]

try:
    r = Render(url)
    html = r.frame.toHtml()

    # need to check url actually matched
    # can compare to <html><head></head><body></body></html>

    matches = re.findall(re.compile(NEW_REGEX), html)
    for m in matches:
        print m[0]

except:
    print "Something went wrong"

