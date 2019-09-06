#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


import secret


#------
# name: config.py
# date: 2016JAN21
# prog: pr
# desc: secret configuration for flickr oauth 
# urls: <https://www.flickr.com/help/forum/72157632667188299/?search=user+id> ¬
#       <http://idgettr.com>
#------
ON  = True
OFF = False
DEBUG = OFF

# flickr generated
api_key = secret.api_key 
api_secret = secret.api_secret

# personal prefs
data_format = 'json'
per_page = '10'
user_name = 'bootload'
user_id = '27164277@N00'

# default photo info
photo_id = '23848891000'

## vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
