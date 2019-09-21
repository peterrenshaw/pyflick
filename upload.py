#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: upload.py
# date: 2019SEP21
#       2019SEP06
#       2019AUG11
#       2016JAN21
# prog: pr
# desc: upload a file to flickr via CLI
# TODO: requires metatag included in process.py
# algo: 
#       upload
#         given a filename
#         given a list of tags
#         given a list of date tags (automated)
#       upload the image given valid filepathname to flickr.
#
# urls: <https://github.com/sybrenstuvel/flickrapi/blob/master/doc/4-uploading.rst>
#       <https://stuvel.eu/flickrapi-doc/4-uploading.html>
#       <https://www.flickr.com/groups/api/discuss/72157675855698367/?search=app+permissions>
#       <https://stuvel.eu/flickrapi-doc/3-auth.html>
#       <https://docs.python.org/2/howto/sorting.html>
#======


import login
import tools
import config

import sys
import os.path
import flickrapi
from optparse import OptionParser


params = {}
params['fileobj'] = None


#---------
# filepath2title: convert filepath (unix) to a filename
#                 use os.path.basename to extract info
#---------
def filepath2title(fpn):
    # convert from /some/filepath/filename.jpg
    #         to   filename
    # HACK add     '.00'
    if fpn: 
        title = os.path.basename(fpn)
        title = title.split('.')

        # yyyymmmddhh.00.jpg OR some_filename.jpg?
        if len(title) > 1: 
            t = "{}.{}".format(title[0], title[1])
        else:
            t = "{}".format(title[0])

        return t
    else:
        return ""
  
#----------
# name: FileWithCallback
# desc: allow file uploading with callback for progress
#----------
class FileWithCallback(object):
    def __init__(self, filename, callback):
        print("fn <{}>".format(filename))
        self.file = open(filename, 'rb')
        self.callback = callback

        # the following attributes and methods are required
        self.len = os.path.getsize(filename)
        self.fileno = self.file.fileno
        self.tell = self.file.tell

    def read(self, size):
        if self.callback:
            self.callback(self.tell() * 100 // self.len)
        return self.file.read(size)

def callback(progress):
    #print(progress)
    pass


#---------
# name: process
# desc: given the parameters, process a list of urls
#       and upload them.
# TODO: find todays date in YYYY,YYYYMMM format and add as 
#       default tags
#---------
def process(params=params):
    print("user <{}> ({})".format(config.user_name, config.user_id))
    print("authenticating...")
    flickr = login.authenticate()

    if flickr:
        print("ok")
        if params['filename']: 
            print("processing <{}>".format(params['filename']))

            params['title'] = filepath2title(params['filename'])
            if not params['tags']: params['tags'] = """2019 2019AUG 2019AUG11"""
            if not params['description']: params['description'] = ""

            params['fileobj'] = FileWithCallback(params['filename'], callback)
            rsp = flickr.upload(fileobj=params['fileobj'],
                                filename=params['filename'],
                                title=params['title'],
                                description=params['description'],
                                tags=params['tags'])

            print("status: <{}>".format(rsp)) 
        else:
            print("Warning: no file found")
            f = None
            pass

        f = None
    else:
        print("Error: Authentication problems")
        f = None
        sys.exit(1)


#---------
# desc: main cli method
# TODO  include ^-l^ option
#---------
def main():
    """cli entry point"""
    usage = "usage: %prog -i -o [-t -d -j -e]"
    parser = OptionParser(usage)

    #------ in/out ------
    parser.add_option("-i", "--input", dest="input",
                      help="input source directory")
    parser.add_option("-j", "--jpg", dest="jpg",
                      action="store_true", 
                      help="process only jpg files")
    parser.add_option("-d", "--description", dest="description", 
                      help="add a description to the the image")
    parser.add_option("-e", "--title", dest="title", 
                      help="add a title to the the image")
    parser.add_option("-t", "--tags", dest="tags", 
                      help="add tags to the the image")

    #------ options ------ 
    options, args = parser.parse_args()  

    #------ process ------
    if options.input:
        # only load 'jpg' images
        print("path: <{}>".format(options.input))
        if options.jpg:
            afiles = tools.get_fn_jpg(options.input)
        else:
            afiles = tools.get_filenames(options.input)
        print("AFILES <{}>".format(afiles))

        print("directory: ({}) <{}>".format(len(afiles), afiles))
        if len(afiles) > 1: 

            # set tags OR defaults
            if options.tags:
                params['tags'] = options.tags
            else:
                tags = ""

            # set title OR nothing
            if options.title:
                params['title'] = options.title
            else:
                title = ""

            # set description OR nothing
            if options.description:
                params['description'] = options.description
            else:
                description = ""      

            # loop through the list of files
            afs = sorted(afiles)
            for fn in afs:
                if fn:
                    if os.path.exists(fn):
                        # process the files one by one
                        params['filename'] = fn
                        params['title'] = filepath2title(fn)
                        process(params)
                    else:
                        print("warning: the source file is not found")
                        print("         <{}>".format(fpn))
                        pass
                else:
                    break        
        else:
            # load all files found
            fpn = os.path.join(os.curdir, options.input)
            fn = options.input

            # parameters
            params['filename'] = fpn
            params['title'] = filepath2title(fpn)
            params['description'] = options.description
            params['tags'] = options.tags

            # check filepathname
            if os.path.exists(fpn):
                print("fpn <{}>".format(fpn))
                process(params)
            else:
                print("error: the source file is not found")
                print("       <{}>".format(fpn))


#----- main cli entry point ------
if __name__ == "__main__":
    main()



# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab

