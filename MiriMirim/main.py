import threading, json, os
from MiriMirim.alarm import *
from MiriMirim.firstRun import *
from MiriMirim.Program import *
alarm_interval = 30

def startProgram(myInfo):
    program = Program(myInfo)
    tray_thread = threading.Thread(target=program.setup, daemon=True)
    alarm_thread = threading.Thread(target=alarm_function, args=(alarm_interval, notification_icon_path,), daemon=True)
    alarm_thread.start()
    tray_thread.start()
    program.main_program()

    print("프로그램이 완전히 종료 중입니다.")

if __name__ == "__main__":
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.abspath(os.path.dirname(__file__))

    userInfoPath = os.path.join(bundle_dir, "../userInfo")
    if len(os.listdir(userInfoPath)) == 0:
        first_run()
    else:
        f = open(userInfoPath+"/myInfo.json", 'r')
        myInfo = json.loads(f.read())
        startProgram(myInfo)





