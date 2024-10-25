import hashlib
import time
from os import walk


folderToCheck = "potion_game"


def calculate_file_hash(file_path):
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash

f = {}
for (dirpath, dirnames, files) in walk(folderToCheck):
    for item in files:
        # exclude this file, if this file is in the base folder. exclude all non py files
        if ".py" in item and item != "git.py":
            f.update({str(item): calculate_file_hash( dirpath + "\\" +item )})
    break

print(len(f))
for value in f:
    print(value)
#calculate_file_hash( walk(folderToCheck) )