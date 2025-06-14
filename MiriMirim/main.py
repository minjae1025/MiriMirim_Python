from Program import *

def programLoad():
    myInfo = myinfoLoad()
    settings = settingLoad()
    main_start(myInfo, settings)

if __name__ == "__main__":
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.abspath(os.path.dirname(__file__))

    userInfoPath = os.path.join(bundle_dir, "source/user")
    if not os.path.isdir(userInfoPath):
        os.mkdir(userInfoPath)

    if os.path.isfile(userInfoPath + "/myInfo.json"):
        programLoad()
    else:
        first_start()
        programLoad()

