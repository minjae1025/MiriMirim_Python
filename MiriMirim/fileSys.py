import json

# userName = input("이름 입력: ")
# userGrade = input("학년 입력: ")
# userClass = input("반 입력: ")
file_path = '../userInfo/myInfo.json'

def save(userName, userGrade, userClass):
    myInfo = { 'userName': userName,
               'userGrade': userGrade,
               'userClass': userClass
               }
    f = open(file_path, 'w')
    f.write(json.dumps(myInfo))
    f.close()

def load():
    f = open(file_path, 'r')
    myInfo = json.loads(f.read())
    print(myInfo)
    return myInfo