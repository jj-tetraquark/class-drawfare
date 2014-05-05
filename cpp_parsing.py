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
        print match.group(1)
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
    contents = get_contents_between_braces(
        file_contents, opening_brace_position)

    contents = strip_comments(contents)
    methods = get_methods(contents)
    members = get_members(contents)
    access_ranges = get_access_specifier_ranges(contents)
    print access_ranges

    specified_methods = list()
    for method in methods:
        method_location = method[0]
        method_name = method[1]
        for access in access_ranges:
            if method_location > access[0] and method_location < access[1]:
                specified_methods.append((access[2], method_name))

    specified_members = list()
    for member in members:
        member_location = member[0]
        member_name = member[1]
        for access in access_ranges:
            if member_location > access[0] and member_location < access[1]:
                specified_members.append((access[2], member_name))

    return {"methods": specified_methods, "members": specified_members}


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


def strip_comments(code):
    removed_single = re.sub('//.*', '', code)  # single line comments
    return re.sub('/\*(.*?)\*/', '', removed_single, 0, re.DOTALL)  # multiline


def get_methods(code):
    method_regex = re.compile(
        r"(friend |unsigned |const |static )*?"  # keywords
        r"([A-Z_a-z0-9]*::)*?"           # scoping and namespaces
        r"[A-Z_a-z0-9~]*\s+"             # type
        r"[A-Z_a-z0-9]*\s*?\([^)]*?\)",   # method name
        re.M)
    matches = method_regex.finditer(code)
    methods = list()
    for match in matches:
        method = re.sub('\n', '', match.group()).strip()
        methods.append((match.start(), method))

    return methods


# TODO - this is incomplete - still doesn't match single line declarations
# e.g. int member1, member2, member3;
def get_members(code):
    member_regex = re.compile(
        r"(friend |unsigned |const |static )*?"  # keywords
        r"([A-Z_a-z0-9]*::)*?"                   # scoping and namespaces
        r"[A-Z_a-z0-9~]+\s+"                     # type
        r"[A-Z_a-z0-9];",                        # member name
        re.M)
    matches = member_regex.finditer(code)
    members = list()
    for match in matches:
        member = re.sub('\n', '', match.group()).strip()
        members.append((match.start(), member))

    return members


def get_access_specifier_ranges(code):
    specifier_keyword_matches = re.finditer(
        r'(public|protected|private)\s*:', code)

    keyword_locations = list()
    for match in specifier_keyword_matches:
        specifier = (match.group()[:-1]).strip()  # strip whitespace and colon
        keyword_locations.append((match.start(), specifier))
    keyword_locations.sort()

    end_of_code = len(code)
    ranges = list()

    previous_key_location = 0
    previous_key_value = 'private'  # private access by default
    for keyword in keyword_locations:
        ranges.append((previous_key_location, keyword[0], previous_key_value))
        previous_key_location = keyword[0]
        previous_key_value = keyword[1]

    last_one = keyword_locations[-1]
    ranges.append((last_one[0], end_of_code, last_one[1]))

    return ranges
