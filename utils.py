import json


def create_json_file(filename, dictionary):
    with open(filename, 'w') as file:
        json.dump(dictionary, file)