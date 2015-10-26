import sys
import re
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  

# Regular expressions for pattern matching
EMAIL_REGEX = '(\w+(\.\w*)*@\w+(\.\w*)+)'

# Class that renders a webpage, allowing JS elements to load
# Code for this class was pulled from from 
#       webscraping.com/blog/Scraping-JavaScript-webpages-with-webkit/
# Module is licenced under LGPL, so I'm allowed to use it
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


# Purpose:   when given a body of text (such as HTML), return a list of
#            all the emails hidden inside
# Arguments: regex-searchable string (body of webpage)
# Returns:   list of unique email addresses
def pull_emails(body):
    matches = re.findall(re.compile(EMAIL_REGEX), body)
    emails = []
    for m in matches:
        emails.append(m[0])

    emails = list(set(emails))

    return emails


# Purpose:   when given a body of text (such as HTML), and a URL, return a 
#            list of URLs within the given domain that are linked in the
#            body
# Arguments: regex-searchable string (body of webpage), string (URL of
#            webpage passed in as body)
# Returns:   list of unique URLs linked within the body
# Note:      Currently determines websites 'in the domain' by looking for
#            relative paths in href element. Does not work for any absolute
#            paths in body
def pull_links(body, base_url):
    return []

# Function that, when given a URL, finds and prints the email addresses
# on the website
def scrape_and_search(base):
    # Stack to keep track of pages to possibly visit
    pages = [base]

    # Dict to keep track of pages already visited
    visited = {}

    while pages:
        url = pages.pop()

        try:
            r = Render(url)
            html = r.frame.toHtml()
            
            # need to check url actually matched
            # can compare to <html><head></head><body></body></html>
            # if not, continue

            emails = pull_emails(html)
            for email in emails:
                print email

            new_links = pull_links(html, url)
            for link in new_links:
                if not link in visited:
                    visited[link] = 'visited'
                    pages.add(link)

        except:
            print "Something went wrong"

#################################################

if len(sys.argv) != 2:
    print "USAGE: python scrape.py [url]"
    sys.exit(0)

# Format so requests recognizes
url = "http://" + sys.argv[1]
scrape_and_search(url)

