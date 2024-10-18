from os import walk
import re

# for fun UML generator, tries to read the files as-is, although some stuff would be easier if there was a tagging system.
folderToCheck = "potion_game"

# convert the result from a regex findall to a list object because it doesn't automatically do that for some reason.
def regexToList(input) -> list:
    l = []
    for item in input:
        if type(item) != str:
            for a in item:
                if a != "":
                    l.append(a)
        else:
            l.append(item)
    l = ' '.join(l).split()
    return l

# find all the files in the base folder
f = []
for (dirpath, dirnames, files) in walk(folderToCheck):
    for item in files:
        # exclude this file, if this file is in the base folder. exclude all non py files
        if ".py" in item and item != "createUml.py":
            f.append(item)
    break
print(f)

# read each file for defs
info = []
for file in f:
    classString = ""
    with open(folderToCheck + "\\" + file, 'r') as opened:
        d = {}
        info.append(d)
        for line in opened:
            if "def" in line:
                pass

            # new class found
            if "class" in line and ":" in line:
                # extract class name, will capture an empty string as well. lets filter it out
                temp = re.findall(r'((?<=\s).*?(?=\())|((?<=[^\S\r\n]).*?(?=:))', line)
                className = regexToList(temp)[0]
                info.append({"class": str(className)})
                info[-1].update({"file": str(file)})
                
                if "(" and ")" in line:
                    # extract subclass names
                    temp = re.findall(r'(?<=\().*?(?=\))', line)
                    info[-1].update({"subclasses": regexToList(temp)})
            
            # functions
            if "def" in line and ":" in line:
                # extract functions
                temp = re.findall(r'(?<=def ).*?\n', line)
                if "function" not in info[-1]:
                    info[-1].update({"function": []})
                string = "".join(temp).split("#", 1)[0].rstrip()
                info[-1].get("function").append(string)
                # TODO extract return type

                        
out = open(folderToCheck + "\\" + "generatedUML.txt", "w")
out.write("@startuml\n")
subclassing = []
for item in info:
    # write down class info
    if "class" in item:
        out.write("class " + item.get("class") + " {\n")
        out.write("From file: " + item.get("file") + "\n")
        
        # write down functions
        for func in item.get("function"):
            # TODO im just going to assume that everything is public.
            out.write("\t+ " + func + "\n")
        out.write("}\n")

        # put subclassing into a buffer for later since afaik standard is that 
        # aggregation/composition/inheritence is placed at the bottom of the file.
        if "subclasses" in item:
            for subc in item.get("subclasses"):
                subclassing.append(subc + " <|-- " + item.get("class"))

for item in subclassing:
    out.write(item + "\n")
out.write("@enduml")
out.close()



