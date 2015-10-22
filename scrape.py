import requests
import sys

if len(sys.argv) != 2:
    print "USAGE: python scrape.py [url]"
    sys.exit(0)

# Format so requests recognizes
url = "http://" + sys.argv[1]

try:
    r = requests.get(url)
    print r.content
except:
    print "Domain could not be accessed"

