# Ben-Ryder 2019
# Currently using JSON as method of level save

import json
import os


def save(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file)


def load(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


def delete(filename):
    os.remove(filename)


def check_exists(filename):
    return os.path.isfile(filename)
