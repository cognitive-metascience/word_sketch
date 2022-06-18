#packages needed: beautifulsoup4, lxml
from bs4 import BeautifulSoup
import os
import re

def read_xml(path_from, save=False, path_to=None):
    with open(path_from, 'r', encoding="utf-8") as f:
        #read and parse data
        data = f.read()
        Bs_data = BeautifulSoup(data, "xml")
        w_orth = Bs_data.find_all('orth') #list of all 'orth' instances

        #clean and put into a string
        res = ""
        for w in w_orth:
            result = re.search('<orth>(.*?)</orth>', str(w))
            word = str(result.group(1))
            if word in ['.', ',', ';', ':', '/', '?', '!',
                        'em', 'am', 'śmy', 'ście', 'm']:
                res += word
            else:
                res += (" " + word)

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

        return res.strip() #space at the beginning

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