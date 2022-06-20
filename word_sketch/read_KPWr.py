#packages needed: lxml

import os
import xml.etree.ElementTree as ET

def read_xml(path_from, save=False, path_to=None):
    #read file and return a list of words
    tree = ET.parse(path_from)
    root = tree.getroot()
    words = []
    for child in root:
        for child2 in child:
            for child3 in child2:
                element = child3.find('orth')
                if element is not None:
                    words.append(str(element.text))
                else:
                    words.append('ns/')

    #put into a string with or without spaces
    res = ''
    add_space=True
    for word in words:
        if word != 'ns/':
            if add_space:
                res += ' ' + word
            else:
                res += word
            add_space=True
        if word == 'ns/':
            add_space=False


    #save data to file (optional)
    if save:
        file_path = os.path.dirname(path_from) + '/' #np. files/KPWr/ - to the same directory
        if path_to is not None:
            file_path = path_to #path defined by user
        file_name = os.path.basename(path_from)[:-3] + 'txt' #np. 00101717.txt
        full_path = file_path+file_name

        out_file = open(full_path, 'w', encoding="utf-8")
        out_file.write(res.strip())
        out_file.close()

    return res.strip()

# 1) save to string
#Wikipedia
wikipedia_zefir = read_xml("files/KPWr/00101187.xml")
print(wikipedia_zefir)
#blog
print(read_xml("files/KPWr/00102314.xml"))

# 2) print and save as .txt file in the same dir as .xml file
#print(read_xml("files/KPWr/00101717.xml", True))
# 3) save to another dir
#read_xml("files/KPWr/00101717.xml", True, "files/")