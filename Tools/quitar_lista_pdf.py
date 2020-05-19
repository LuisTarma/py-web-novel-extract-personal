from bs4    import BeautifulSoup as BS
import os

HREF_START_WITH = "https://www.skynovels.net/read-offline"
WORKING_FOLDER = os.getcwd()
FILE_NAME_BASE = "index"

def buscarLinks(soup):
    text = ""
    for a in soup.find_all("a"):
        try:
            link = a["href"]
            if link.startswith(HREF_START_WITH):
                text += link
                text += "\n"
        except KeyError:
            continue
    return text

def __init__():
    output = open("salida.txt", "w")
    
    fix_folder = WORKING_FOLDER + "\\"
    file_list = []
    folder_data = os.scandir(WORKING_FOLDER)
    for f in folder_data:
        if f.is_file and f.name.startswith(FILE_NAME_BASE):
            file_list.append(fix_folder + f.name)
    
    txt_output = ""
    for i in file_list:
        html = open(i)
        soup = BS(html, "html.parser")
        txt_output += buscarLinks(soup)
        print("Listo.."+ i)
    
    output.write(txt_output)
    output.close()
    print("Done..")

__init__()