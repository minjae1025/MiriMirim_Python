import json

class Account():
    Name = ""
    myGrade = int
    myClass = int
    timeTable = [["" for _ in range(5)] for _ in range(7)]
    workTimes = ["08:25", "09:25", "10:25", "11:25", "12:18", "13:15", "14:15", "15:15"]
    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    setting = {
            'dark' : False,
            'alarm' : True,
            'background' : True
        }


    def __init__(self, myInfo, settings):
        self.Name = myInfo["userName"]
        self.myGrade = int(myInfo["userGrade"])
        self.myClass = int(myInfo["userClass"])
        self.settings = settings

    def getmyGrade(self):
        return self.myGrade

    def getmyClass(self):
        return self.myClass

    def getworkTimes(self):
        return self.workTimes

    def setSettings(self, settings):
        self.settings = settings




