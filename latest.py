#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: latest.py
# date: 2016JAN21
# prog: pr
# desc: get back the latest image from flickr
# urls: 
#======

import sys
import json
import flickrapi


import login
import config


def latest():
    print("user <{}> ({})".format(config.user_name, config.user_id))
    if login.authenticate():
        print("ok")

        # do stuff
        # extract the latest image
        flickr = flickrapi.FlickrAPI(config.api_key, config.api_secret, format=config.data_format)
        raw_json = flickr.photos_search(user_id=config.user_id, per_page='1')
        photos = json.loads(raw_json.decode('utf-8'))

        for key in photos.keys():
            if key == 'photos':
                print(photos[key])

        return True
    else:
        print("authentication failure")
        return False

def main():
    """cli entry point"""
    latest()

#----- main cli entry point ------
if __name__ == "__main__":
    main()


## vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab

