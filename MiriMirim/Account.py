import json

class Account():
    Name = ""
    myGrade = int
    myClass = int
    Timetable = [[0 for _ in range(7)] for _ in range(5)]
    workTimes = ["08:30", "09:30", "10:30", "11:30", "12:20", "13:20", "14:20", "15:20"]

    def __init__(self, myInfo):
        self.Name = myInfo["userName"]
        self.myGrade = int(myInfo["userGrade"])
        self.myClass = int(myInfo["userClass"])

    def set_timetable(self, timetable):
        self.Timetable = timetable




