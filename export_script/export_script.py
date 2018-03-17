# User pyinstaller to compile any changes

import os, sys, shutil
from bs4 import BeautifulSoup

script_dir = sys.argv[0]
export_dir = sys.argv[1]

for currentDirPath, subDirList, fileList in os.walk(export_dir):
    currentDirName = currentDirPath.split("\\")[-1]
    if currentDirName != "templates" and currentDirName != "static":
        for filename in fileList:
            if ".html" in filename:
                shutil.copy(currentDirPath + "\\" + filename, export_dir + "\\templates\\" + filename)
            elif ".css" in filename or ".js" in filename or ".png" in filename or ".jpg" in filename:
                shutil.copy(currentDirPath + "\\" + filename,  export_dir + "\\static\\" + filename)
            os.remove(currentDirPath + "\\" + filename)

# Remove old directories
shutil.rmtree(export_dir + "\\assets")

# Auto-Template html files

# Being cool ;P
html_files = [currentDirPath + "\\" + filename for filename in fileList for currentDirPath, subDirList, fileList in os.walk(export_dir + "\\templates")]

for html_file in html_files:
    # Open file for read/write
    file = open(html_file, "r")

    soup = BeautifulSoup(file, 'html.parser')
    for script in soup.findAll("script"):
        script["src"] = "{{ url_for('static', filename=%s) }}" % (script["src"].split("/")[-1])
    for image in soup.findAll("img"):
        print(image)
    for link in soup.findAll("link"):
        if link["rel"][0] == "stylesheet":
            link["href"] = "{{ url_for('static', filename=%s) }}" % (link["href"].split("/")[-1])

    file.close()

    file = open(html_file, "w")
    file.write(str(soup.prettify()))
    file.close()




