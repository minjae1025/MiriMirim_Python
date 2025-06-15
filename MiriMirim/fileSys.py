import json, sys, os
from PIL import Image
from PyQt5 import uic
from PyQt5.QtCore import Qt, QCoreApplication, QFile, QTextStream, QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    bundle_dir = sys._MEIPASS

else:
    bundle_dir = os.path.abspath(os.path.dirname(__file__))

user_path = os.path.join(bundle_dir, 'source/user/')
img_path = os.path.join(bundle_dir, 'source/img/')
gui_path = os.path.join(bundle_dir, 'source/gui/')

image_path = os.path.join(bundle_dir, img_path, 'miri_mirim.ico')
notification_icon_path = image_path
image = Image.open(image_path)

mainUi = uic.loadUiType(os.path.join(bundle_dir, gui_path, 'mainWindow.ui'))[0]
firstUi = uic.loadUiType(os.path.join(bundle_dir, gui_path, 'firstWindow.ui'))[0]

def myinfoSave(userName, userGrade, userClass):
    myInfo = { 'userName': userName,
               'userGrade': userGrade,
               'userClass': userClass
               }
    f = open(user_path+'myInfo.json', 'w')
    f.write(json.dumps(myInfo))
    f.close()
    return True

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