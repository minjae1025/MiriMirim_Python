import threading
from program.alarm import *
from program.gui import *

if __name__ == "__main__":

    alarm_interval = 30

    alarm_thread = threading.Thread(target=alarm_function, args=(alarm_interval, notification_icon_path,), daemon=True)
    alarm_thread.start()

    tray_thread = threading.Thread(target=setup_tray_icon, daemon=True)
    tray_thread.start()

    main_program()

    print("프로그램이 완전히 종료 중입니다.")