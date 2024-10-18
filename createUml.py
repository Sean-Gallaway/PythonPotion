from os import walk
import re

f = []
for (dirpath, dirnames, files) in walk("potion_game"):
    for item in files:
        if "UML" not in item and item != "createUml.py":
            f.append(item)
    break
print(f)

# read each file for defs
classes = []
for file in f:
    classString = ""
    with open("potion_game\\" + file, 'r') as opened:
        for line in opened:
            if "def" in line:
                pass

            # new class found
            if "class" in line:
                # extract class name, will capture an empty string as well. lets filter it out
                className = re.findall(r'((?<=\s).*?(?=\())|((?<=[^\S\r\n]).*?(?=:))', line)
                while "" in className:
                    className.remove("  ")
                print(type(className[0]))
                
                if "(" and ")" in line:
                    # extract subclass names
                    test = re.findall(r'(?<=\().*?(?=\))', line)
                    
print(classes)