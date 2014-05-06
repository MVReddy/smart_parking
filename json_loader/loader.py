import json

def json_to_dict(filename):
    dictionary = None
    try:
        with open(filename) as filename:
            dictionary = json.loads(filename.read())
    except IOError:
        print("Cannot open file {}".format(filename))
    
    return dictionary
