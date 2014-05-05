#! /usr/bin/env python
import sys
import os
from termcolor import cprint, colored
from cpp_parsing import get_header_files, find_class_declarations_in_file

if len(sys.argv) is not 2:
    cprint("Incorrect usage", color='red')
    print("You must specify a root of a C++ project like so:\n"
          "\tclass-drawfare path/to/project/")
    exit()

rootdir = sys.argv[1]

if not os.path.isdir(rootdir):
    cprint("Error: Not a valid directory", color='red', file=sys.stderr)


if __name__ == "__main__":
    # get all header files
    header_files = get_header_files(rootdir)

    classList = list()
    for filename in header_files:
        find_class_declarations_in_file(filename, classList)

    for cppClass in classList:
        filename = colored(cppClass.filename, 'green')
        print filename + " : %d " % cppClass.position,
        cprint("%s [%s]" % (cppClass.name, cppClass.inherits), attrs=['bold'])
        print cppClass.contents
