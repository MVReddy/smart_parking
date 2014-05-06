import json

filename = "paths.json"

try:
    with open(filename) as paths_file:
        paths = json.loads(paths_file.read())
        sections = paths["sections"]
        for section in sections:
            print section["path_from_start"]
#            slots = section["slots"]
#            for slot in slots: 
#                print slot["id"] 
        
             
except IOError:
    print("Cannot open map file {}".format(filename))
