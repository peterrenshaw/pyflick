#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#------
# name: config.py
# date: 2019SEP06
#       2016JAN21
# prog: pr
# desc: secret configuration for flickr oauth 
# urls: <https://www.flickr.com/help/forum/72157632667188299/?search=user+id> ¬
#       <http://idgettr.com>
#------


import secret


ON  = True
OFF = False
DEBUG = ON

# flickr generated
api_key = secret.api_key 
api_secret = secret.api_secret

# personal prefs
data_format = 'json'
per_page = '10'
user_name = secret.user_name
user_id = secret.user_id

# default photo info
photo_id = secret.photo_id


## vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
