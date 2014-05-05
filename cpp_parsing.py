import os
import re
from cpp_class import CPP_Class


def get_header_files(root_directory):
    header_file_list = list()
    for root, subdirs, files in os.walk(root_directory):
        for filename in files:
            if re.match(r'[A-Za-z_0-9\-]+\.h', filename):
                header_file_list.append(os.path.join(root, filename))
    return header_file_list


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
                get_class_contents(file_contents, match.end()-1),
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


def get_class_contents(file_contents, opening_brace_position):
    return get_contents_between_braces(file_contents, opening_brace_position)


def get_contents_between_braces(file_contents, opening_brace_position):
    brace_counter = 0
    for pos, character in enumerate(file_contents[opening_brace_position:]):
        if character is '{':
            brace_counter += 1
        elif character is '}':
            brace_counter -= 1

        if brace_counter is 0:
            closing_brace_position = opening_brace_position + pos + 1
            return file_contents[opening_brace_position:closing_brace_position]
