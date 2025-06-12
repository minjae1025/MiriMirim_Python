from alarm import *
from Program import *

alarm_interval = 30

def startProgram(myInfo):
    global program
    alarm_thread = threading.Thread(target=alarm_function, args=(alarm_interval, notification_icon_path,), daemon=True)
    alarm_thread.start()
    main_start(myInfo)

def first_run():
    first_start()

if __name__ == "__main__":
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.abspath(os.path.dirname(__file__))

    userInfoPath = os.path.join(bundle_dir, "source/userInfo")
    if len(os.listdir(userInfoPath)) == 0:
        first_run()
        f = open(userInfoPath + "/myInfo.json", 'r')
        myInfo = json.loads(f.read())
        startProgram(myInfo)
    else:
        f = open(userInfoPath+"/myInfo.json", 'r')
        myInfo = json.loads(f.read())
        startProgram(myInfo)
