EmailHunt
=========

You give me a domain, and I'll scrape those emails.

#### Usage: python scrape_class.py [url]
[url] is a domain

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
> __python scrape_class.py [url] > output_file__ 
and opening the __output_file__ afterward is the best way to parse
through annoying stderr messages
* When the website uses scrunched-up CSS that has no whitespace, the
tool sometimes finds strings in the CSS that match my email regular
expression

(coming soon)
