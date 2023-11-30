#!/usr/bin/env python

"""
    usage: python iMessage.py <DestinationFolder>
"""

import os
import sys
import hashlib
import shutil
import exifread
from datetime import datetime
from random import randint
import argparse

# lists for later use
src_dict = {}  # source
dst_dict = {}  # destination
non_exif_filenames = []  # FileNames without EXIF

# Path to iMessage directory, based upon User Login
path = "/Users/" + os.getlogin() + "/Library/Messages/Attachments/"

# return HASH value for file
def md5(fname):
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()

# Return the File Extension
def imageType(rawname):
    return os.path.splitext(rawname)[1]


# prevent duplicate filenames
def rename_pics(filename, rawName):
 
    f = open(filename, 'rb')
    processed = exifread.process_file(f)
    stripped = str(processed.get('Image DateTime'))
    if processed.get('Image DateTime') is not None:
        dt = datetime.strptime(stripped, '%Y:%m:%d %H:%M:%S')
        return '{2:02}-{1}-{0}_{03}.{04}.{05}'.format(dt.day, dt.month,
                                                      dt.year, dt.hour,
                                                      dt.minute, dt.second) \
                                                      + imageType(rawName)
    else:
        return str(randint(0, 999999)) + "-" + rawName


# Create a dictionary with contents of the directory. The HASH value (unique) is used as 
# the dictionary key and filename and path as values associated to the key
def populate_dict(directory, diction):

    for root, dirs, files in os.walk(directory):
        for name in files:
            if str(name).endswith((".jpg", ".JPEG", ".JPG", ".PNG", ".png")):
                newName = rename_pics(os.path.abspath(os.path.join
                                                     (directory, root, name)),
                                     name)
                diction[md5(os.path.abspath(os.path.join(directory,
                            root, name)))] = name, \
                    os.path.abspath(os.path.join(directory, root, name)), \
                    newName
    return diction

# Rename the files in the destination
def rename(oldName, newName, destination):

    return os.rename((destination) + "/" + str(oldName), (destination) + "/" + str(newName))

# copy files
def copy_files(destination):

    for key in list(src_dict.keys()):
        if key in dst_dict:
            pass
        else:
            value = src_dict[key]
            shutil.copy(value[1], destination)
            rename(value[0], value[2], destination)


# Main
def main(argv):
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Destination folder path for your photos")
    args = parser.parse_args()
    populate_dict(path, src_dict)
    populate_dict(args.folder, dst_dict)
    copy_files(args.folder)

if __name__ == "__main__":
    main(sys.argv)

