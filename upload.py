#!/usr/bin/env python3
# ~*~ encoding: utf-8 ~*~


#======
# name: upload.py
# date: 2019OCT26
#       2019SEP21
#       2019SEP06
#       2019AUG11
#       2016JAN21
# prog: pr
# desc: upload a file to flickr via CLI
#
#
#   ./upload.py       -i $HOME/work/flickr/2019/2019SEP/2019SEP21/u1/*.png 
#                     -t """bootload 2019 2019SEP 2019SEP21 climate change climatestrip australia temperatures 
#                           temp hot data warmingstripe 1901 2018"""
#                     -d "Warming Stripes for #Australia from 1901-2018 Using data from Berkeley Earth. #ShowYourStripes"
#
#
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
import argparse


PROG_NAME = 'upload'
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
def process(flickr_login, params=params):
    print("user <{}> ({})".format(config.user_name, config.user_id))
    print("authenticating...")
    flickr = flickr_login

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

def process_batch(flickr_login, afiles, params=params):
    """
    upload a whole lot of files at once with one connection, not open-close
    for each one
    """
    print("user <{}> ({})".format(config.user_name, config.user_id))
    print("authenticating...")
    flickr = flickr_login

    # loop through sorted list of files
    afs = sorted(afiles)
    count = len(afs)
    for fn in afs:
        if fn:
           if os.path.exists(fn):
                # process the files one by one
                params['filename'] = fn
                params['title'] = filepath2title(fn)
            
                # process all the files
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
                        flickr = None
                        pass
                else:
                    print("Error: Authentication problems")
                    f = None
                    flickr = None
                    sys.exit(1)

           # does filenamepath exist?
           else:
               print("warning: the source file is not found")
               print("         <{}>".format(fpn))
               pass
        # is there a file to process?
        else:
            break        
    
    # done
    flickr = None
    print("batch ({}) done".format(count))


#---------
# desc: main cli method
# TODO  include ^-l^ option
#---------
def main():
    """cli entry point"""
    parser = argparse.ArgumentParser(usage='%(prog)s [options]')

    #------ in/out ------
    parser.add_argument("-i", "--input", dest="input",
                      help="input source directory")
    parser.add_argument("-j", "--jpg", dest="jpg",
                      action="store_true", 
                      help="process only jpg files")
    parser.add_argument("-d", "--description", dest="description", 
                      help="add a description to the the image")
    parser.add_argument("-e", "--title", dest="title", 
                      help="add a title to the the image")
    parser.add_argument("-t", "--tags", dest="tags", 
                      help="add tags to the the image")
    parser.add_argument("-v", '--version', dest='version',
                      action="store_true",
                      help="Version information")
    #--------- options --------- 
    args = parser.parse_args()
    if not args:
        parser.print_help()
        sys.exit(1)

    #--------- version ---------
    if args.version:
        print("{} {}".format(sys.argv[0], '0.1'))
        sys.exit(1)


    #-=------- process ---------
    if args.input:
        # only load 'jpg' images
        print("path: <{}>".format(args.input))
        if args.jpg:
            afiles = tools.get_fn_jpg(args.input)
        else:
            afiles = tools.get_filenames(args.input)

        print("AFILES <{}>".format(afiles))
        print("directory: ({}) <{}>".format(len(afiles), afiles))

        if len(afiles) > 1: 
            # set tags OR defaults
            if args.tags:
                params['tags'] = args.tags
            else:
                tags = ""

            # set title OR nothing
            if args.title:
                params['title'] = args.title
            else:
                title = ""

            # set description OR nothing
            if args.description:
                params['description'] = args.description
            else:
                description = ""      

            # authenticate ONCE, then upload
            # looped list of files
            flickr = login.authenticate()
            process_batch(flickr, afiles, params)
            flickr = None

        else:
            # load all files found
            fpn = os.path.join(os.curdir, args.input)
            fn = args.input

            # parameters
            params['filename'] = fpn
            params['title'] = filepath2title(fpn)
            params['description'] = args.description
            params['tags'] = args.tags

            # check filepathname
            if os.path.exists(fpn):
                print("fpn <{}>".format(fpn))

                # process one file
                flickr = login.authenticate()
                process(flickr, params)
                flickr = None
            else:
                print("error: the source file is not found")
                print("       <{}>".format(fpn))


#--------- main cli entry point ---------
if __name__ == "__main__":
    main()



# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab

