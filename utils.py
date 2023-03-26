import json


def create_json_file(filename, dictionary):
    with open(filename, 'w') as file:
        json.dump(dictionary, file)


def name_clean(name_string):
    name_as_list = [*name_string]
    name = ''
    for i,char in enumerate(name_as_list[::-1]):
        if i == 0 and char == "." or char == ",":
            continue
        else:
            if char == ' ':
                name += "-"
            else:
                name += char
    return name[::-1]