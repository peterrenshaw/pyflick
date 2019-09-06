#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~

#======
# name: ftoy.py
# date: 2016JAN21
# prog: pr
# desc: test login for flickr api
# urls: <https://docs.python.org/3/library/json.html>
#======


import json
import flickrapi


import config


print("user <{}> ({})".format(config.user_name, config.user_id))

flickr = flickrapi.FlickrAPI(config.api_key, config.api_secret, format=config.data_format)
photos = flickr.photos.search(user_id=config.user_id, per_page=config.per_page)
raw_json = flickr.photosets.getList(user_id=config.user_id)
parsed = json.loads(raw_json.decode('utf-8'))


print('data ({})'.format(len(parsed)))
for key in parsed.keys():
    print('{}={}'.format(key, parsed[key]))


def main():
    """cli entry point"""
    pass

#----- main cli entry point ------
if __name__ == "__main__":
    main()


## vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab

