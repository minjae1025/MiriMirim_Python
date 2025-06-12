import json, sys, os

# userName = input("이름 입력: ")
# userGrade = input("학년 입력: ")
# userClass = input("반 입력: ")
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    bundle_dir = sys._MEIPASS

else:
    bundle_dir = os.path.abspath(os.path.dirname(__file__))

file_path = os.path.join(bundle_dir, 'source/userInfo/myInfo.json')

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