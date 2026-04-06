import json, sys, os
from PIL import Image
from PyQt5 import uic
from PyQt5.QtCore import Qt, QCoreApplication, QFile, QTextStream, QThread, pyqtSignal, QTimer
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
    file_path = os.path.join(user_path, 'myInfo.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(myInfo, f, ensure_ascii=False, indent=4)
    return True

def myinfoLoad():
    file_path = os.path.join(user_path, 'myInfo.json')
    if not os.path.exists(file_path):
        return None  # 파일이 없을 경우 예외 처리

    with open(file_path, 'r', encoding='utf-8') as f:
        myInfo = json.load(f)  # json.loads(f.read()) 보다 효율적
        print(myInfo)
        return myInfo

def settingLoad():
    if os.path.isfile(user_path+'settings.json'):
        with open(user_path+'settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
            return settings
    else:
        return {
            'dark' : False,
            'alarm' : True,
            'background' : True
        }

def settingSave(settings):
    with open(user_path + 'settings.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)
    return True