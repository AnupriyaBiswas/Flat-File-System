import json

def read_json_metadata(path):
    with open(path) as f:
        return json.load(f)

def write_json_metadata(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
