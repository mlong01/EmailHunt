# find_email_addresses.py
# 
# Written by:       Matt Long
# Last modified:    10/26/15
#
# Purpose:          Given a domain, prints out a list of all email addresses 
#                   that can be found on the given page as well as its child
#                   pages.

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

# Code for this class was modified by me but originally found on
# https://webscraping.com/blog/Scraping-multiple-JavaScript-webpages-with-webkit/
# Module is licenced under LGPL, so I'm allowed to use it (I'm pretty sure)
#
# Class that renders a webpage, allowing JS-rendered elements to load and then
# be scraped by the tool

class Render(QWebPage):  
  def __init__(self, urls, cb):
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    
    # list of urls to scrape through - added to during execution
    self.urls = urls  

    # callback so all HTML bodies don't have to be stored in memory
    self.cb = cb

    # dictionaries of urls and emails to prevent duplication
    self.visited_sites = {}
    self.found_emails = {}

    self.crawl()  
    self.app.exec_()  


  # called after init finishes setup    
  def crawl(self):  
    if self.urls:  
      url = self.urls.pop(0)  
      self.mainFrame().load(QUrl(url))  
    else:  
      self.app.quit()  


  # fires after page loads in crawl function          
  def _loadFinished(self, result):  
    frame = self.mainFrame()  
    url = str(frame.url().toString())  
    html = frame.toHtml()  
    
    emails, urls = self.cb(url, html)

    for email in emails:
        if not email in self.found_emails:
            self.found_emails[email] = 'found'
            print email

    for url in urls:
        if not url[1] in self.visited_sites:
            self.visited_sites[url[1]] = 'visited'
            self.urls.append(url[0])
    
    self.crawl()  


# Purpose:   when given a url and a body of text (such as HTML), return
#            email addresses found on page as well as child pages on site
# Arguments: regex-searchable string (body of webpage), string (URL of
#            webpage passed in as body)
# Returns:   a tuple containing a list of email addresses and a list of
#            absolute urls to search in future iterations
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if len(sys.argv) != 2:
    print "USAGE: python scrape.py [url]"
    sys.exit(0)

urls = [sys.argv[1]]

r = Render(urls, cb=scrape_and_search)

