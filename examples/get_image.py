#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from urllib2 import quote
from base64 import urlsafe_b64encode


#url = "http://localhost:8000/resize/?url=%s&x=50&y=50" % (quote("http://dajool.com/public/images/dajool_badge.png"), )
url = "http://localhost:8000/thumbnail/%s/50/50/" % (urlsafe_b64encode("http://dajool.com/public/images/dajool_badge.png"), )

request = requests.get(url)
print request.content
