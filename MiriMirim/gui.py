import sys, os, threading
from datetime import datetime, timedelta
from PIL import Image
from PyQt5 import uic
from PyQt5.QtCore import *
from fileSys import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from MiriMirim.requestApi import requestApi
from MiriMirim.Account import Account
tray_icon = None

#UI파일 연결
firstUi = uic.loadUiType("../gui/firstWindow.ui")[0]
mainUi = uic.loadUiType("../gui/mainWindow.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class firstWindowClass(QMainWindow, firstUi) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('미리미림')
        self.setWindowIcon(QIcon('../img/miri_mirim.ico'))
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
        self.setWindowIcon(QIcon('../img/miri_mirim.ico'))
        self.setFixedSize(1600, 900)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.btnMain)
        self.button_group.addButton(self.btnSetting)
        self.button_group.addButton(self.btnMyInfo)
        self.button_group.setExclusive(True)  # 한 번에 하나의 버튼만 체크 가능

    # 창을 보여주는 함수
    def show_window(self):
        print("창을 표시합니다.")
        self.showNormal()  # 윈도우를 일반 상태(최대화/최소화 아님)로 표시
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
        today = datetime.today()
        for i in range(0, 5):
            day = today + timedelta(days=-today.weekday()+i)
            j = 0
            try:
                data = requestApi(day.strftime("%Y%m%d"), self.my.myGrade, self.my.myClass)
                for item in data:
                    self.my.Timetable[i][j] = item
                    j += 1
            except Exception as e:
                print(e)
                #tk.Label(frame, text=f"API 데이터 로딩 오류: {e}").pack()

        for item in self.my.Timetable:
            print(item)

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.abspath(os.path.dirname(__file__))

image_path = os.path.join(bundle_dir, '../img', 'miri_mirim.ico')
notification_icon_path = image_path
image = Image.open(image_path)