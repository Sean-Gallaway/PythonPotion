import hashlib
import os
from os import walk
import subprocess


folderToCheck = "potion_game"
fileExtensions = ["py", "txt"]

confirmations = ["y", "yes"]

# modified from https://www.geeksforgeeks.org/how-to-detect-file-changes-using-python/
def calculate_file_hash(file_path):
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash

# find all python files in this project.
f = {}
cwd = ""
for (dirpath, dirnames, files) in walk(folderToCheck):
    cwd = dirpath
    for item in files:
        # check if file has extensions we want to save.
        temp = item.split(".")
        if temp[1] in fileExtensions:
            f.update({str(item): calculate_file_hash( dirpath + "\\" +item )})
    break
# set our working directory for git commands later.
os.chdir(cwd)

# slightly modified from https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-the-currently-running-scrip
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
manifest_old = open(os.path.join(__location__, "git_manifest.txt"), 'r')

# check the manifest to see if the hashes are the same.
any_changes = False
for line in manifest_old:
    storedFile = line.split(" ");
    if storedFile[0] in f:
        if storedFile[1] != f.get(storedFile[0].rstrip()):
            print( subprocess.run("git stage " + storedFile[0]) )
            any_changes = True
    else:
        f.update({storedFile[0]: storedFile[1]})
manifest_old.close()

# if any changes detected, ask if they want to commit staged changes
if any_changes:
    ask_commit = input("commit?\n")
    if ask_commit in confirmations:
        commit_message = input("Give a commit message below:\n")
        subprocess.run("git commit -m \"" + commit_message + "\"")

# ask to save the manifest to git_manifest.txt
ask_save = input("save manifest?\n")
if ask_save in confirmations:
    print("manifest saved")
    manifest_new = open("git_manifest.txt", "w")
    for key, value in f.items():
        manifest_new.write(key + " " + value + " \n")

# ask to commit to the repo
ask_push = input("Commit?\n")
if ask_push in confirmations:
    print("pushing")
    subprocess.run("git push")