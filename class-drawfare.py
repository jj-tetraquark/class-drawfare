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

def get_header_files(root_directory):
    header_file_list = list()
    for root, subdirs, files in os.walk(root_directory):
        for filename in files:
            if re.match(r'[A-Za-z_0-9\-]+\.h', filename):
                header_file_list.append(os.path.join(root,filename))
    return header_file_list

def find_class_declarations_in_file(filename):
    file_contents = open(filename, 'r').read()
    match = re.search(
            r'^(?!enum).*class\b\s(\b[A-Za-z_][A-Za-z_0-9]*\b)\s*[$]?(:[$]?\s*[public|protected|private]\s*[^{]*\s*)?{',
        file_contents, re.M)
    if match:
        print match.groups()


# get all header files
header_files = get_header_files(rootdir)

for filename in header_files:
    find_class_declarations_in_file(filename)
