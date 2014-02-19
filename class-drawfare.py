#! /usr/bin/env python

import sys, os, re
from termcolor import cprint, colored

if len(sys.argv) is not 2:
    cprint("Incorrect usage", color='red')
    print("You must specify a root of a C++ project like so:\n"
          "\tclass-drawfare path/to/project/")
    exit()

rootdir = sys.argv[1]

if not os.path.isdir(rootdir):
    cprint("Error: Not a valid directory", color='red', file=sys.stderr)

def get_header_files(root_directory):
    header_file_list = list()
    for root, subdirs, files in os.walk(root_directory):
        for filename in files:
            if re.match(r'[A-Za-z_0-9\-]+\.h', filename):
                header_file_list.append(os.path.join(root,filename))
    return header_file_list


class Cpp_class:
    def __init__(self, name, filename, inherits):
        self.name = name
        self.filename = filename
        self.inherits = inherits

def find_class_declarations_in_file(filename, classList):
    file_contents = open(filename, 'r').read()
    matches = re.findall(
        r'^(?!enum).*class\b\s(\b[A-Za-z_][A-Za-z_0-9]*\b)\s*[$]?(:[$]?\s*[public|protected|private]\s*[^{]*\s*)?{',
        file_contents, re.M)
    for match in matches:
        classList.append(Cpp_class(match[0], filename, match[1]))
         


# get all header files
header_files = get_header_files(rootdir)

classList = list()
for filename in header_files:
    find_class_declarations_in_file(filename, classList)


for cppClass in classList:
    filename = colored(cppClass.filename, 'green')
    print filename + " : ",
    cprint(cppClass.name, attrs=['bold'])
