import pandas as pd
import numpy
class Locker(object):
    def __init__(self):
        lockers = self.readFile("newfirstfloor.csv")
        students = self.readFile("listofstudent.csv")
        students = students.values
        lockers = lockers.values
        out = self.fillLockers(students,lockers)
        self.exportAsCSV(out)
    def readFile(self,loc):
        df = pd.read_csv(loc)
        return df
    def fillLockers(self,students,lockers):
        output = []
        lockers = numpy.array(lockers).tolist()
        for i in students:
            locknum = -1
            for f in lockers:
                if(i[1] == f[1]):
                    output.append([f[0],i[0],i[1]])
                    locknum = f
                    break
            if(locknum != -1):
                lockers.remove(locknum)
            else:
                output.append(['Not Found',i[0],i[1]])
        print(output)
        return output
    def exportAsCSV(self,output):
        df = pd.DataFrame(output)
        df.columns=['Locker Number','Student Numbers','Class']
        df.to_csv("output.csv",index=False)
locker = Locker()
