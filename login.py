#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~

#======
# name: login.py
# date: 2019SEP06
#       2016JAN21
# prog: pr
# desc: test login for flickr api
# urls: <https://docs.python.org/3/library/json.html>
#======


import flickrapi
import webbrowser


import config


#------
# name: authenticate <https://bitbucket.org/sybren/flickrapi/src/875f0705db20743580364706a13bba4cb0d60d7e/doc/3-auth.rst?at=default&fileviewer=file-view-default>
#------
def authenticate(user_name =  config.user_name, 
                 user_id =    config.user_id,
                 api_key =    config.api_key,
                 api_secret = config.api_secret,
                 debug =      config.DEBUG):
    """flickr authentication process"""

    if debug:
        print("log into flickr")
        print("user <{}> ({})".format(user_name, user_id))
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    if debug: 
        print("authorising...")

    if not flickr.token_valid(perms='write'):
        if debug:
            print('\trequest token')
        flickr.get_request_token(oauth_callback='oob')
     
        if debug: 
            print('\topen browser at authentication url')
        authorize_url = flickr.auth_url(perms='write')
        webbrowser.open_new_tab(authorize_url)

        if debug:
            print('\tget verifier code to user')
        verifier = input('Verifier code: ')
 
        if debug: 
            print('\ttrade the request token for access token')
        flickr.get_access_token(verifier)

        if debug:
            print("success")
    else:
        if debug: 
            print("user {} granted access".format(user_name))

    return flickr

def main():
    """cli entry point"""
    authenticate()

#----- main cli entry point ------
if __name__ == "__main__":
    main()


## vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab

