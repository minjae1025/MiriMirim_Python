import json, sys, os

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    bundle_dir = sys._MEIPASS

else:
    bundle_dir = os.path.abspath(os.path.dirname(__file__))

user_path = os.path.join(bundle_dir, 'source/user/')

def myinfoSave(userName, userGrade, userClass):
    myInfo = { 'userName': userName,
               'userGrade': userGrade,
               'userClass': userClass
               }
    f = open(user_path+'myInfo.json', 'w')
    f.write(json.dumps(myInfo))
    f.close()

def myinfoLoad():
    f = open(user_path+'myInfo.json', 'r')
    myInfo = json.loads(f.read())
    print(myInfo)
    return myInfo

def settingLoad():
    if os.path.isfile(user_path+'settings.json'):
        f = open(user_path + 'settings.json', 'r')
        settings = json.loads(f.read())
        return settings
    else:
        return {
            'dark' : False,
            'alarm' : True,
            'background' : True
        }

def settingSave(settings):
    f = open(user_path+'settings.json', 'w')
    f.write(json.dumps(settings))
    f.close()
    return True