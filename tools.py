#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: tools.py
# date: 2019AUG11
#       2016FEB03
# prog: pr
# desc: tools for image processing
# urls: PIL
#       <https://github.com/python-pillow/Pillow>
#       <https://pillow.readthedocs.org/en/latest/handbook/index.html>
#
#       datetime
#       <http://strftime.org/>
#       <http://pleac.sourceforge.net/pleac_python/datesandtimes.html>
#======


import sys
import glob
import time
import os.path
import datetime


#------ date time start -----

#------
# desc: datetime string in YYYY MMM DD HH MM SS format
#       and display as "YYYYMMMDDTHH:MM.SS", components
#       are the following:
#       YYYY = %Y  -- full 4 digit year
#       MMM  = %b  -- truncated month, UC
#       DD   = %d  -- day, zero padded
#       HH   = %H  -- 24 hour, zero padded
#       MM   = %M  -- minute, zero padded
#       SS   = %S  -- second, zero padded
#------
DTF_YYYYMMMDDTHHMMSS = "%Y%b%dT%H:%M.%S"

def dt_date2str(dt, dt_format=DTF_YYYYMMMDDTHHMMSS):
    """convert a valid date time to a string format"""
    if dt_format:
        dts = dt.strftime(dt_format)
        return dts
    else:
        return ""
def dt_get_now(is_utc=True):
    """return current, now  date time"""
    if is_utc:
        return datetime.datetime.utcnow()
    else:
        return datetime.datetime.now()
def dt2epoch(dt):
    """
    given datetime object, return epoch
    be aware of the differences b/w now 
    utc_now (local time and UTC time)
    """
    e = time.mktime(dt.timetuple())
    return e
def dt_build_date(yyyy, mmm, dd, hh=0, mm=0, ss=0):
    """
    build datetime obj from year, month, day, hour, min, seconds 
    """
    dt = datetime.datetime(yyyy, mmm, dd, hh, mm, ss)
    return dt
#------ date time end ------

#------ extract filenames start ------
def get_filenames(filepath, file_type="*.*"):
    """
    given a valid filepath, gather all 
    the files in that directory as a list
    by globbing them using glob.glob. Use
    file_type to restrict or wild-card the 
    types of files to select.
    """
    #print("get_filenames.filepath <{}>".format(filepath))
    filepathdir = os.path.dirname(filepath)

    if os.path.isdir(filepathdir):
       fpn = os.path.join(filepathdir, file_type)
       files = glob.glob(fpn)

       print("fpn <{}>".format(fpn))
       print("get_filenames <{}>".format(files))
 
       return files
    else:
       return []
def get_fn_jpg(filepath):
    return get_filenames(filepath, "*.jpg")
def get_fn_jpeg(filepath):
    return get_filenames(filepath, "*.jpeg")
def get_fn_png(filepath):
    return get_filenames(filepath, "*.png")
#------ extract filenames end ------

def main():
    """cli entry point"""
    pass

#----- main cli entry point ------
if __name__ == "__main__":
    main()


## vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab

