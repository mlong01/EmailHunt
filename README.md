EmailHunt
=========

You give me a domain, and I'll scrape those emails.

#### Prerequisites:

This tool requires the PyQt4 library, which must be installed.
To install on Ubuntu, run

> `sudo apt-get install python-qt4`


#### Usage: 

> `python scrape_class.py [url]`

[url] is a domain that _includes_ the protocol, meaning include `http://` or 
`https://` in your url. For example, `https://airbnb.com` is a great url

#### Acknowledgements:
[This
post](https://webscraping.com/blog/Scraping-multiple-JavaScript-webpages-with-webkit/),
 written by Richard Penman, is what I found to be the most reliable, least-
external-package/library dependent method for rendering a webpage and
all of its dynamic content for scraping in python. My render class is
based heavily on his, with a couple tweaks to allow for dynamic
building of the list of urls to search.

Honorable mentions for other tools that possibly could have been used include:
* [Ghost.py](https://github.com/jeanphix/Ghost.py)
* [PhantomJS](http://phantomjs.org/)
* [SlimerJS](https://slimerjs.org/)
* [Selenium](http://www.seleniumhq.org/)
* [Splash](https://github.com/scrapinghub/splash)



#### Known bugs/shortcomings
* The tool can only find child pages linked by a relative _href_.
Anything linked absolutely cannot be found as of yet.
* While the tool can find content registered by javascript, there is
no guarantee that content relying on an asynchronous AJAX request will
be rendered and therefore captured
* Modules inside the PyQt4 library have print messages to stderr when
it finds issues with HTML/CSS that it renders - for an example, try
what I imagine will be the first website you'll test this on... For now,
piping the program to a file when run by running 
`python scrape_class.py [url] > output_file` 
and opening the `output_file` afterward is the best way to parse
through annoying stderr messages
* When the website uses scrunched-up CSS that has no whitespace, the
tool sometimes finds strings in the CSS involving selectors with `@` 
that match my email regular expression, and inaccurately return them 
as emails - for example, I've found `shadow@2x.png` which looks like
it could be an email if `.png` was an acceptable top-level domain name 

