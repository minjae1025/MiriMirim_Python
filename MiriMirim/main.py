from Program import *

def startProgram(myInfo):
    global program
    main_start(myInfo)

if __name__ == "__main__":
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.abspath(os.path.dirname(__file__))


    userInfoPath = os.path.join(bundle_dir, "source/user")
    if not os.path.isdir(userInfoPath):
        os.mkdir(userInfoPath)

    if os.path.isfile(userInfoPath + "/myInfo.json"):
        f = open(userInfoPath + "/myInfo.json", 'r')
        myInfo = json.loads(f.read())
        startProgram(myInfo)
    else:
        first_start()
        f = open(userInfoPath + "/myInfo.json", 'r')
        myInfo = json.loads(f.read())
        startProgram(myInfo)

