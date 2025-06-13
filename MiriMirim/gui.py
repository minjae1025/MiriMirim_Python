import sys, os, threading, time
from datetime import datetime, timedelta
from PIL import Image
from PyQt5 import uic
from PyQt5.QtCore import *
from fileSys import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from requestApi import requestApi
from Account import Account
from plyer import notification
from datetime import datetime
tray_icon = None

img_path = 'source/img'
gui_path = 'source/gui'

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    bundle_dir = sys._MEIPASS

else:
    bundle_dir = os.path.abspath(os.path.dirname(__file__))

image_path = os.path.join(bundle_dir, img_path, 'miri_mirim.ico')
notification_icon_path = image_path
image = Image.open(image_path)

#UI파일 연결
#os.path.join(bundle_dir, '../gui', 'firstWindow.ui')
firstUi = uic.loadUiType(os.path.join(bundle_dir, gui_path, 'firstWindow.ui'))[0]
mainUi = uic.loadUiType(os.path.join(bundle_dir, gui_path, 'mainWindow.ui'))[0]

#화면을 띄우는데 사용되는 Class 선언
class firstWindowClass(QMainWindow, firstUi) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('미리미림')
        self.setWindowIcon(QIcon(image_path))
        self.setFixedSize(1600, 900)


    def start(self) :
        userName = self.nameText.text()
        userGrade = self.gradeCombo.currentText()
        userClass = self.classCombo.currentText()

        if userName == '' :
            QMessageBox.warning(self, '미리미림', '이름을 입력해주세요!')
            return
        if userGrade == '학년' or userClass == '반':
            #print("학년과 반을 선택해 주세요")
            QMessageBox.warning(self, '미리미림', '학년과 반을 선택해 주세요')
            return

        save(userName, userGrade, userClass)
        self.close()

class MainWindowClass(QMainWindow, mainUi) :
    def __init__(self, myInfo) :
        super().__init__()
        self.my = Account(myInfo)
        self.setupUi(self)
        self.setWindowTitle('미리미림')
        self.setWindowIcon(QIcon(image_path))
        self.setFixedSize(1600, 900)

        alarm_interval = 10
        alarm_thread = threading.Thread(target=self.alarm_function, args=(alarm_interval, notification_icon_path,), daemon=True)
        alarm_thread.start()

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.btnMain)
        self.button_group.addButton(self.btnSetting)
        self.button_group.addButton(self.btnMyInfo)
        self.button_group.setExclusive(True)  # 한 번에 하나의 버튼만 체크 가능

        self.tabs.tabBar().hide()

        self.btnMain.clicked.connect(lambda: self.tabs.setCurrentWidget(self.timetableWidget))
        self.btnSetting.clicked.connect(lambda: self.tabs.setCurrentWidget(self.settingWidget))
        self.btnMyInfo.clicked.connect(lambda: self.tabs.setCurrentWidget(self.myinfoWidget))
        self.btnMain.setChecked(True)

        self.tabs.setCurrentWidget(self.timetableWidget)
        self.timetable.itemChanged.connect(self.update_data)
        self.timetable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.timetable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_data(self, item: QTableWidgetItem):
        row = item.row()
        col = item.column()
        new_value = item.text()

        # 데이터 배열의 유효성 검사 (인덱스 범위 확인)
        if 0 <= row < len(self.my.timeTable) and 0 <= col < len(self.my.timeTable[row]):
            # 파이썬 배열 업데이트
            self.my.timeTable[row][col] = new_value
            print(f"데이터 업데이트: timetable[{row}][{col}] = '{self.my.timeTable[row][col]}'")
        else:
            print(f"Error: Row {row}, Col {col} out of bounds for data array.")

    # 창을 보여주는 함수
    def show_window(self):
        print("창을 표시합니다.")
        self.showNormal()  # 윈도우를 일반 상태로 표시
        self.activateWindow()  # 윈도우 활성화
        self.raise_()  # 윈도우를 맨 앞으로 가져옵니다.

    #창을 숨기는 함수
    def hide_window(self):
        print("창을 숨깁니다.")
        self.hide()

    def quit_application(self):
        print("프로그램이 완전히 종료되었습니다.")
        if tray_icon:
            tray_icon.hide() # 트레이 아이콘 숨기기
        QCoreApplication.quit() # PyQt 애플리케이션 종료

    def closeEvent(self, event):
        print("윈도우 닫기 이벤트 감지.")
        self.hide_window()  # 윈도우를 숨깁니다.
        event.ignore() # 창을 숨김

    def setup_tray_icon(self):
        global tray_icon
        app_icon = QIcon(image_path)

        tray_icon = QSystemTrayIcon(app_icon, self)
        tray_icon.setToolTip("미리미림") # 툴팁 설정
        tray_icon.activated.connect(self.on_tray_icon_activated)

        # 트레이 메뉴 생성
        tray_menu = QMenu()

        # 창 열기 액션
        open_action = QAction("창 열기", self)
        open_action.triggered.connect(self.show_window)
        tray_menu.addAction(open_action)

        # 숨기기 액션
        hide_action = QAction("숨기기", self)
        hide_action.triggered.connect(self.hide_window)
        tray_menu.addAction(hide_action)

        # 종료 액션
        quit_action = QAction("종료", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)

        tray_icon.setContextMenu(tray_menu)

        tray_icon.show() # 트레이 아이콘 표시

    def on_tray_icon_activated(self, reason):
        # 트레이 아이콘이 클릭되었을 때 (Trigger)
        if reason == QSystemTrayIcon.Trigger:
            self.show_window()

    def main_program(self):
        table_widget = self.timetable
        today = datetime.today()
        for i in range(0, 5):
            day = today + timedelta(days=-today.weekday()+i)
            j = 0
            try:
                data = requestApi(day, self.my.myGrade, self.my.myClass, )
                if data == "error":
                    QMessageBox.critical(self, '인터넷 오류!', '인터넷이 오류로 인한 프로그램 실행에 실패했습니다. 프로그램을 종료합니다.')
                    exit(1)
                for item in data:
                    subject = item[1:-1]
                    self.my.timeTable[j][i] = subject
                    j += 1
            except Exception as e:
                print(e)

        try:
            for row_idx, row_data in enumerate(self.my.timeTable):
                for col_idx, item_data in enumerate(row_data):
                        item = QTableWidgetItem(str(item_data))  # QTableWidgetItem 생성
                        item.setTextAlignment(Qt.AlignCenter)
                        table_widget.setItem(row_idx, col_idx, item)  # 테이블에 아이템 설정
        except Exception as e:
            print(f"시간표 출력중 에러 발생 : {e}")

    def alarm_function(self, interval_seconds, icon_path):
        today = datetime.today().weekday()
        workTimes = self.my.getworkTimes()
        row = 0
        nextTimeIdx = 0
        current_time = datetime.now().time()
        if today == 0 or today == 4:
            length = 7
        elif today == 5 or today == 6:
            notification.notify(
                title='미리미림',
                message=str(f"오늘은 주말입니다!"),
                app_name='미리미림 알리미',
                app_icon=icon_path,
                timeout=5
            )
            return
        else:
            length = 8

        for item in workTimes:
            if datetime.strptime(item, "%H:%M").time() < current_time:
                nextTimeIdx += 1
                row += 1

        while True:
            today = datetime.today().weekday()
            column = today
            print(nextTimeIdx)
            current_time = datetime.now().time()
            print(current_time)
            if nextTimeIdx < length:
                parsed_time = datetime.strptime(workTimes[nextTimeIdx], "%H:%M").time()

                if current_time > parsed_time:
                    next = self.my.timeTable[row][column]
                    if "*" in next or "프로그래밍" in next:
                        subject = f"전공 수업인 {next}"
                    elif "체육" in next or "운동" in next:
                        subject = f"신나는 {next}"
                    else:
                        subject = f"{next}"
                    try:
                        if nextTimeIdx == 4:
                            message = "곧 점심시간입니다!"
                        else:
                            message = f"다음 교시는 {subject}입니다. 미리 준비하세요!"
                            row += 1

                        notification.notify(
                            title='미리미림',
                            message=message,
                            app_name='미리미림 알리미',
                            app_icon=icon_path,
                            timeout=5
                        )
                    except Exception as e:
                        print(f"알림 실패: {e} ")
                    nextTimeIdx += 1

            time.sleep(interval_seconds)