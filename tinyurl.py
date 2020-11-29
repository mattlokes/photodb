#!/usr/bin/env python3 
import contextlib 
import sys 

try:
    from urllib.parse import urlencode		 
except ImportError:
    from urllib import urlencode 

try:
    from urllib.request import urlopen 
except ImportError:
    from urllib2 import urlopen 

def create_one(url):
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8 ')									 
if __name__ == '__main__':
    for tinyurl in map(create_one, sys.argv[1:]):
        print(tinyurl)

