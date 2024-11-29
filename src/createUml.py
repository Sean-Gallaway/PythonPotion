from os import walk
import re

# for fun UML generator, tries to read the files as-is, although some stuff would be easier if there was a tagging system.
folderToCheck = "potion_game//src"
lineCount = 0

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

# read each file for defs
info = []
for file in f:
    classString = ""
    with open(folderToCheck + "\\" + file, 'r') as opened:
        for line in opened:
            lineCount += 1
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
                    if "Enum" in info[-1].get("subclasses"):
                        info[-1].update({ "class": ("enum " + str(info[-1].get("class"))) })
            
            # functions
            if "def" in line and ":" in line:
                if len(re.findall(r"(\t|\s.)def.*", line)) == 0:
                    info.append({"class": "GLOBAL_" + str(file)})
                    info[-1].update({"file": str(file)})

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
        if "enum " not in item.get("class"):
            out.write("class " + item.get("class") + " {\n")
        elif "enum " in item.get("class"):
            out.write(item.get("class") + " {\n")
        out.write("From file: " + item.get("file") + "\n")
        
        # write down functions
        if "function" in item:
            for func in item.get("function"):
                # TODO im just going to assume that everything is public.
                out.write("\t+ " + func + "\n")
        out.write("}\n")

        # put subclassing into a buffer for later since afaik standard is that 
        # aggregation/composition/inheritence is placed at the bottom of the file.
        if "subclasses" in item:
            for subc in item.get("subclasses"):
                if subc != "Enum":
                    subclassing.append(subc + " <|-- " + item.get("class"))
    else:
        print(item)

for item in subclassing:
    out.write(item + "\n")
out.write("@enduml")
out.close()


print(lineCount)
