#! /usr/bin/env python

import sys, os, re

if len(sys.argv) is not 2:
    print("\tIncorrect usage\n"
          "\tYou must specify a root of a C++ project like so:\n"
          "\t\tclass-drawfare path/to/project/")
    exit()

rootdir = sys.argv[1]

if not os.path.isdir(rootdir):
    print("Error: Not a valid directory")

# get all header files
for root, subdirs, files in os.walk(rootdir):
    for filename in files:
        if re.match(r'[A-Za-z_0-9\-]+\.h', filename):
            print os.path.join(root,filename)
