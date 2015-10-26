import requests
import sys

# Any num of non-whitespace chars followed by @ followed by a word
# followed by a '.' followed by another word
EMAIL_REGEX = '\S*@\w*.\w*'

if len(sys.argv) != 2:
    print "USAGE: python scrape.py [url]"
    sys.exit(0)

# Format so requests recognizes
url = "http://" + sys.argv[1]

try:
    r = requests.get(url)
    print r.content
    # ISSUE - does not work on JS-rendered sites
except:
    print "Domain could not be accessed"

