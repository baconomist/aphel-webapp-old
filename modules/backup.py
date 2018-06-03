import datetime
import shutil
import os
import collections
import json
import time
## TODO:Delete backups every.. x amount of days

class Backup(object):
    def __init__(self,files : list,folders : list,init, interval : list):
        self.files = files
        self.interval = collections.defaultdict(lambda :0)

        self.interval = interval
        if(init == "now"):
            self.init = self.getCurrTime()
        else:
            self.init = init
        self.folders = folders
        self.loop()

    def loop(self):
        while(True):
            self.checkInterval()
            #To really save performance we will only check every 30 seconds
            time.sleep(30)

    def getCurrTime(self):
        #TODO: Move from system time to some remote server's time
        return datetime.datetime.now()

    #Return True if database is corrupted False if NOT
    def checkDatabaseCorrupted(self,dir):
        try:
            with open(dir) as f:
            #    print (f.read())
                json.loads(f.read())
        except ValueError as e:
            print(e)
            return True
        return False

    #Do the actual backup
    def backup(self):
        print( "Backed UP")

        dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\data"
        tempdir = dir_path + "\\backups\\" + self.getCurrTime().strftime("%Y-%m-%d-%H.%M.%S")
        #Make the directory with the timestamp
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        #Copy all non json files and check if the json files are corrupted
        for d in self.files:
            d2 = dir_path + "\\" + d
            if(d2.endswith('.json') and self.checkDatabaseCorrupted(d2)):
                print('JSON file is corrupted')
            else:
                shutil.copy(d2,tempdir)
        #Copy all folders and archive them
        for f in self.folders:
            shutil.make_archive(f,'zip',tempdir)
            shutil.move(f + ".zip",tempdir)
    #check if the time is greater then the expected time
    def checkInterval(self):
        adjusted = self.init + datetime.timedelta(days=self.interval['days'],hours=self.interval['hours'],minutes=self.interval['minutes'])

        if(adjusted <= self.getCurrTime()):
            self.backup()
            self.init = self.getCurrTime()
            return True
        return False

#Ex. Implementation
#Backup([List of filenames in data],[list of folders to archive in data],put the initial value to count from or "now",how long from the initial date given)
#Right now when you run this script every 12 hours it will backup

b = Backup(['database.json'],['profile_images'],"now",{'hours': 12, 'days': 0,'minutes': 0})
