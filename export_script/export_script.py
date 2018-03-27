# User pyinstaller to compile any changes

import os, sys, shutil
from bs4 import BeautifulSoup

script_dir = sys.argv[0]
export_dir = sys.argv[1]

# test_dir = "C:\\Users\\Lucas\\Desktop\\Projects\\PCHackers\\webapp"
# export_dir = test_dir


# if os.path.exists(export_dir + "\\templates\\"):
# shutil.rmtree(export_dir + "\\templates\\")
# os.makedirs(export_dir + "\\templates\\")
if not os.path.exists(export_dir + "\\templates\\"):
    os.makedirs(export_dir + "\\templates\\")

# if os.path.exists(export_dir + "\\static\\"):
# shutil.rmtree(export_dir + "\\static\\")
# os.makedirs(export_dir + "\\static\\")
if not os.path.exists(export_dir + "\\static\\"):
    os.makedirs(export_dir + "\\static\\")

for currentDirPath, subDirList, fileList in os.walk(export_dir):
    currentDirName = currentDirPath.split("\\")[-1]

    if "templates" not in currentDirPath and "static" not in currentDirPath and "assets" in currentDirPath or currentDirPath == export_dir:
        for filename in fileList:
            if ".html" in filename:
                if not os.path.exists(export_dir + "\\templates\\" + currentDirPath.replace(export_dir, "").replace(
                        "\\assets\\", "")):
                    os.makedirs(
                        export_dir + "\\templates\\" + currentDirPath.replace(export_dir, "").replace("\\assets\\", ""))

                shutil.copy(currentDirPath + "\\" + filename,
                            export_dir + "\\templates\\" + currentDirPath.replace(export_dir, "").replace("\\assets\\",
                                                                                                          "") + "\\" + filename)

                os.remove(currentDirPath + "\\" + filename)

            elif ".css" in filename or ".js" in filename or ".png" in filename or ".jpg" in filename or ".eot" in filename or ".svg" in filename or ".ttf" in filename or ".woff" in filename:
                if not os.path.exists(export_dir + "\\static\\" + currentDirPath.replace(export_dir, "").replace(
                        "\\assets\\", "")):
                    os.makedirs(
                        export_dir + "\\static\\" + currentDirPath.replace(export_dir, "").replace("\\assets\\", ""))

                shutil.copy(currentDirPath + "\\" + filename,
                            export_dir + "\\static\\" + currentDirPath.replace(export_dir + "\\assets\\",
                                                                               "") + "\\" + filename)

                os.remove(currentDirPath + "\\" + filename)

# Remove old directories
if os.path.exists(export_dir + "\\assets"):
    shutil.rmtree(export_dir + "\\assets")

# Auto-Template html files

# Being cool ;P
# html_files = [currentDirPath + "\\" + filename for filename in fileList if ".html" in filename for currentDirPath, subDirList, fileList in os.walk(export_dir + "\\templates")]



html_files = []

for currentDirPath, subDirList, fileList in os.walk(export_dir + "\\templates"):
    for filename in fileList:
        if ".html" in filename:
            html_files.append(currentDirPath + "\\" + filename)

for html_file in html_files:
    # Open file for read/write
    file = open(html_file, "r")

    print(html_file)

    soup = BeautifulSoup(file, 'html.parser')
    for script in soup.findAll("script"):
        try:
            script["src"] = "{{ url_for('static', filename='%s') }}" % (script["src"].replace("assets/", ""))
        except:
            pass
    for image in soup.findAll("img"):
        try:
            image["src"] = "{{ url_for('static', filename='%s') }}" % (image["src"].replace("assets/", ""))
        except:
            pass
    for link in soup.findAll("link"):
        if link["rel"][0] == "stylesheet":
            link["href"] = "{{ url_for('static', filename='%s') }}" % (link["href"].replace("assets/", ""))

    file.close()

    file = open(html_file, "w")
    file.write(str(soup.prettify()))
    file.close()

css_files = []

for currentDirPath, subDirList, fileList in os.walk(export_dir + "\\static"):
    for filename in fileList:
        if ".css" in filename:
            css_files.append(currentDirPath + "\\" + filename)

for css_file in css_files:
    # Open file for read/write
    file = open(css_file, "r")

    data = file.read().replace("../assets/", "").replace("../", "/static/")  # .replace("/static/fonts/", "")

    file.close()

    file = open(css_file, "w")
    file.write(data)
    file.close()






