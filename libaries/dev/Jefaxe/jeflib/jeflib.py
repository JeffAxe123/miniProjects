#this libary was created by Jefaxe
#it includes some handy function, to use thislibary simply download it, put it into the folder your running your script from
#write "import jeflib" then use jefblib.<function> to call functions.

import os
import requests
import urllib


#exceptions
class WebError(Exception):
    pass
def downloadFile(url,filepath,overwrite=False): #makes it easier to download files, only downloads them if they are not already downloaded (unless overwite=True is set)
    if not overwrite:
        if not os.path.exists(filepath):
            r = requests.get(url)
            try:
                if not r.content.decode("utf-8")=="404: Not Found":
                    with open(filepath,'wb') as output_file:
                        output_file.write(r.content)
                    return True
                else:
                    raise WebError("The file said to be at "+url+" returned 404")
                    return False
            except UnicodeError:
                with open(filepath,'wb') as output_file:
                        output_file.write(r.content)
                return True
    if overwite:
        with open(filepath,'wb') as output_file:
                        output_file.write(r.content)

def createFile(filename,contents,overwite=False): #creates a file if it does not exits, otherwise does nothing
    if not os.path.exists(filename) or overwite==True:
        with open(filename):
            crt.write(str(contents))
            return True
    else:
        return False

def createFolder(foldername): #creates a folder (or tree of folder) if it does not exist, otherwise does nothing
    try:
        os.makedirs(foldername)
        return True
    except FileExistsError:
        return False

def replace_line(file_name, line_num, text):#replaces a given line of a given file
    #this function is from stack overflow, https://stackoverflow.com/questions/4719438/editing-specific-line-in-text-file-in-python
        lines = open(file_name, 'r').readlines()
        lines[line_num] = text
        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()


if __name__=="__main__":
    print("Hey! This isn't meant to be run, just import it")
