import json

class Account():
    Name = ""
    myGrade = int
    myClass = int
    timeTable = [["" for _ in range(5)] for _ in range(7)]
    workTimes = ["08:15", "09:15", "10:15", "11:15", "12:05", "12:55", "13:55", "14:55"]
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




