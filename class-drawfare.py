#! /usr/bin/env python
import sys
import os
import re
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
                header_file_list.append(os.path.join(root, filename))
    return header_file_list


class CPP_Class:
    def __init__(self, name, inherits, filename, position):
        self.name = name
        self.inherits = inherits
        self.filename = filename
        self.position = position


def find_class_declarations_in_file(filename, classList):
    file_contents = open(filename, 'r').read()
    class_regex = re.compile(
        r"^(?!enum).*class\b\s(\b[A-Za-z_][A-Za-z_0-9]*\b)\s*[$]?(:[$]?\s*"
        r"[public|protected|private]\s*[^{]*\s*)?{",
        re.M)
    matches = class_regex.finditer(file_contents)
    for match in matches:
        classList.append(
            CPP_Class(
                match.group(1),
                build_inheritance_tuple_list(match.group(2)),
                filename,
                match.start())
            )


def build_inheritance_tuple_list(inheritance_declaration):
    if inheritance_declaration is None:
        return "BASE"

    #remove colon and strip newline
    inheritance_declaration = inheritance_declaration.strip()[1:]
    inheritance_list = inheritance_declaration.split(',')
    tuple_list = list()
    for parent in inheritance_list:
        parent = parent.strip()
        declaration_tuple = parent.split(' ')
        tuple_list.append(declaration_tuple)
    return tuple_list

# get all header files
header_files = get_header_files(rootdir)

classList = list()
for filename in header_files:
    find_class_declarations_in_file(filename, classList)


for cppClass in classList:
    filename = colored(cppClass.filename, 'green')
    print filename + " : %d " % cppClass.position,
    cprint("%s [%s]" % (cppClass.name, cppClass.inherits), attrs=['bold'])
