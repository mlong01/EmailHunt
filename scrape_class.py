import sys, os
import re
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  

# Matches anything of form w.x@y.z ('.x' is optional)
EMAIL_REGEX = '(\w+(\.\w*)*@\w+(\.\w*)+)'

# Used to find relative links in html body
RELATIVE_LINK_FIND_REGEX = 'href="\/[^"]+"'
RELATIVE_LINK_CLEAN_REGEX = '\/[^"]+'

# TODO: regex for finding absolute links

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Class that renders a webpage, allowing JS elements to load
# Code for this class was pulled from from 
#       webscraping.com/blog/Scraping-JavaScript-webpages-with-webkit/
# Module is licenced under LGPL, so I'm allowed to use it
class Render(QWebPage):  
  def __init__(self, urls, cb):
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.urls = urls  
    self.cb = cb
    self.visited = {}
    self.crawl()  
    self.app.exec_()  
      
  def crawl(self):  
    if self.urls:  
      url = self.urls.pop(0)  
      self.mainFrame().load(QUrl(url))  
    else:  
      self.app.quit()  
        
  def _loadFinished(self, result):  
    frame = self.mainFrame()  
    url = str(frame.url().toString())  
    html = frame.toHtml()  
    
    emails, urls = self.cb(url, html)

    for email in emails:
        print email

    for url in urls:
        if not url[1] in self.visited:
            self.visited[url[1]] = 'visited'
            self.urls.append(url[0])
    
    self.crawl()  


# Function that, when given a URL, finds and prints the email addresses
# on the website
def scrape_and_search(url, html):
    emails = pull_emails(html)
    urls = pull_links(url, html)

    return emails, urls


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
def pull_links(base_url, body):
    matches = re.findall(re.compile(RELATIVE_LINK_FIND_REGEX), body)
    links = []
    
    for m in matches:
        rel_path = re.search(re.compile(RELATIVE_LINK_CLEAN_REGEX), m)
   
        if rel_path:
            rel_path = rel_path.group()
            to_append = base_url + rel_path[1:]  # remove leading /
            links.append((to_append, rel_path))
        
    return links



#################################################

if len(sys.argv) != 2:
    print "USAGE: python scrape.py [url]"
    sys.exit(0)

urls = ["http://" + sys.argv[1]]

r = Render(urls, cb=scrape_and_search)

