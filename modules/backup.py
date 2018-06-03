import datetime
import shutil
import os
import collections
import json
import time
class Backup(object):
    def __init__(self,files : list,folders : list, interval : list):
        self.files = files
        self.interval = interval
        self.interval = collections.defaultdict(lambda :0)
        self.init = self.getCurrTime()
        self.folders = folders
    #    self.checkInterval()

    def loop(self):
        while(True):
            self.checkInterval()
            print("Looped")
            time.sleep(100)

    def getCurrTime(self):
        #TODO: Move from system time to some remote server's time
        return datetime.datetime.now()

    #Return True if database is corrupted False if NOT
    #TODO Actually check the database content
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
        print("Intervaled")
        adjusted = self.init + datetime.timedelta(days=self.interval['days'],hours=self.interval['hours'],minutes=self.interval['minutes'])
        if(adjusted <= self.getCurrTime()):
            self.backup()
            return True
        return False

#Ex. Implementation
#You can specify
