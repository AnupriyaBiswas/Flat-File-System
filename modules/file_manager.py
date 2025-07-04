import os

def list_files(directory):
    return os.listdir(directory)

def delete_file(filepath):
    os.remove(filepath)

def read_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def save_file(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)
