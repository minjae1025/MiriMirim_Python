import threading, random, time
from requsetWork import *
from fileSys import *
from Account import Account
from plyer import notification
from datetime import datetime
tray_icon = None
goodPhrase = ['좋은', '즐거운', '행복한', '신나는']

class MainWindowClass(QMainWindow, mainUi) :
    def __init__(self, myInfo, settings) :
        super().__init__()
        self.my = Account(myInfo, settings)
        self.setupUi(self)
        self.setWindowTitle('미리미림')
        self.setWindowIcon(QIcon(image_path))
        self.setFixedSize(1600, 900)

        if (self.my.settings['background']):
            self.setup_tray_icon()

        if (self.my.settings['alarm']):
            alarm_interval = 10
            alarm_thread = threading.Thread(target=self.alarm_function, args=(alarm_interval, notification_icon_path,),daemon=True)
            alarm_thread.start()

        self.worker_thread = None
        self.try_timetable_request()

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

        self.btnSettingSave.clicked.connect(self.apply_setting)
        self.btnSettingDefault.clicked.connect(self.set_default)

        if (self.my.settings['dark']):
            pixmap = QPixmap(img_path+'dark_side_logo.png')
            self.sideLogo.setPixmap(pixmap)
            self.apply_stylesheet("dark.qss")
        else:
            pixmap = QPixmap(img_path+'light_side_logo.png')
            self.sideLogo.setPixmap(pixmap)
            self.apply_stylesheet("light.qss")

        self.set_setting_btn()

        self.darkmode.setTristate(False)
        self.alarm.setTristate(False)
        self.background.setTristate(False)

        self.background.stateChanged.connect(self.change_value)
        self.alarm.stateChanged.connect(self.change_value)
        self.darkmode.stateChanged.connect(self.change_value)

        self.tabs.setCurrentWidget(self.timetableWidget)
        self.timetable.itemChanged.connect(self.update_data)
        self.timetable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.timetable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.gradeCombo.setCurrentIndex(self.my.getmyGrade()-1)
        self.classCombo.setCurrentIndex(self.my.getmyClass()-1)
        self.gradeCombo.setEnabled(False)
        self.classCombo.setEnabled(False)
        self.btnCancelMyinfo.setEnabled(False)

        self.myLabel.setText(f"안녕하세요 {self.my.Name}님!\n {random.choice(goodPhrase)} {self.my.weekdays[datetime.today().weekday()]}요일 보내세요!")
        self.btnSaveMyinfo.clicked.connect(self.set_myinfo)
        self.btnSaveMyinfo.setEnabled(False)
        self.btnEditMyinfo.clicked.connect(self.edit_myinfo)
        self.btnCancelMyinfo.setEnabled(False)
        self.btnCancelMyinfo.clicked.connect(self.cancel_myinfo)

    def change_value(self):
        self.btnSettingSave.setEnabled(True)

    def cancel_myinfo(self):
        self.gradeCombo.setCurrentIndex(self.my.getmyGrade() - 1)
        self.classCombo.setCurrentIndex(self.my.getmyClass() - 1)
        self.gradeCombo.setEnabled(False)
        self.classCombo.setEnabled(False)
        self.btnSaveMyinfo.setEnabled(False)
        self.btnEditMyinfo.setEnabled(True)
        self.btnCancelMyinfo.setEnabled(False)

    def edit_myinfo(self):
        self.gradeCombo.setEnabled(True)
        self.classCombo.setEnabled(True)
        self.btnSaveMyinfo.setEnabled(True)
        self.btnEditMyinfo.setEnabled(False)
        self.btnCancelMyinfo.setEnabled(True)

    def set_myinfo(self):
        userGrade = self.gradeCombo.currentText()
        userClass = self.classCombo.currentText()
        print(userGrade, userClass)
        save = myinfoSave(self.my.Name, userGrade, userClass)
        self.my.myGrade = userGrade
        self.my.myClass = userClass

        self.try_timetable_request()
        self.gradeCombo.setEnabled(False)
        self.classCombo.setEnabled(False)
        self.btnSaveMyinfo.setEnabled(False)
        self.btnEditMyinfo.setEnabled(True)
        self.btnCancelMyinfo.setEnabled(False)
        if save:
            QMessageBox.about(self, '미리미림', '저장 성공!')
        else:
            QMessageBox.critical(self, '미리미림', '저장 실패! 관리자에게 문의하세요.')

    def set_setting_btn(self) :
        self.darkmode.setChecked(self.my.settings['dark'])
        self.alarm.setChecked(self.my.settings['alarm'])
        self.background.setChecked(self.my.settings['background'])
        self.btnSettingSave.setEnabled(False)

    def set_default(self):
        default = QMessageBox.warning(self, '미리미림', '정말 기본값으로 하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
        if default == QMessageBox.Yes:
            self.btnSettingSave.setEnabled(False)
            settings = {
            'dark' : False,
            'alarm' : True,
            'background' : True
            }

            save = settingSave(settings)
            self.set_setting_btn()

            if save:
                QMessageBox.about(self, '미리미림', '기본값으로 저장 성공!')
            else:
                QMessageBox.critical(self, '미리미림', '기본값으로 저장 실패! 관리자에게 문의하세요.')


    def apply_setting(self):
        settings = {
            'dark': self.darkmode.isChecked(),
            'alarm': self.alarm.isChecked(),
            'background': self.background.isChecked()
        }

        save = settingSave(settings)
        self.my.settings['dark'] = settings['dark']
        if self.my.settings['dark']:
            print('다크모드 적용됨')
            pixmap = QPixmap(img_path + 'dark_side_logo.png')
            self.sideLogo.setPixmap(pixmap)
            self.apply_stylesheet("dark.qss")
        else:
            print('라이트모드 적용됨')
            pixmap = QPixmap(img_path + 'light_side_logo.png')
            self.sideLogo.setPixmap(pixmap)
            self.apply_stylesheet("light.qss")

        if save:
            QMessageBox.about(self, '미리미림', '설정 저장 성공!')
        else:
            QMessageBox.critical(self, '미리미림', '설정 저장 실패! 관리자에게 문의하세요.')

    def apply_stylesheet(self, filename):
        path = os.path.join(bundle_dir, 'source/gui/')
        file = QFile(path+filename)
        if not file.open(QFile.ReadOnly | QFile.Text):
            print(f"Error: Could not open stylesheet file: {filename}")
            return
        stream = QTextStream(file)
        stylesheet = stream.readAll()
        self.centralwidget.setStyleSheet(stylesheet)  # QApplication에 스타일 시트 적용
        file.close()

    def update_data(self, item: QTableWidgetItem):
        row = item.row()
        col = item.column()
        new_value = item.text()

        # 데이터 배열의 유효성 검사 (인덱스 범위 확인)
        if 0 <= row < len(self.my.timeTable) and 0 <= col < len(self.my.timeTable[row]):
            # 파이썬 배열 업데이트
            self.my.timeTable[row][col] = new_value
            # print(f"데이터 업데이트: timetable[{row}][{col}] = '{self.my.timeTable[row][col]}'")
        else:
            QMessageBox.critical(self, '미리미림', '오류! 시간표 수정 실패')

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

    def closeEvent(self, closeEvent):
        print("윈도우 닫기 이벤트 감지.")
        if (self.my.settings['background']):
            self.hide_window()  # 윈도우를 숨깁니다.
            closeEvent.ignore()
        else:
            re = QMessageBox.question(self, "미리미림", "종료 하시겠습니까?")
            if re == QMessageBox.Yes:
                print("프로그램을 종료합니다.")
                exit(1)
            else:
                closeEvent.ignore()


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

    def try_timetable_request(self):
        if self.worker_thread and self.worker_thread.isRunning():
            print("이전 스레드가 아직 실행 중입니다. 중지 후 재시작합니다.")
            self.worker_thread.stop()  # 이전 스레드를 안전하게 중지

        # print(f"새로운 데이터 로딩 시작 요청: 파라미터 = {self.my.getmyGrade()}, {self.my.getmyClass()}")
        self.worker_thread = None
        self.worker_thread = DataWorker(self.my.getmyGrade(), self.my.getmyClass())
        self.worker_thread.data_loaded.connect(self.show_timetable)
        self.worker_thread.start()

    def show_timetable(self, received_data):
        self.my.timeTable = received_data
        table_widget = self.timetable
        try:
            for row_idx, row_data in enumerate(self.my.timeTable):
                for col_idx, item_data in enumerate(row_data):
                        item = QTableWidgetItem(str(item_data))  # QTableWidgetItem 생성
                        item.setTextAlignment(Qt.AlignCenter)
                        table_widget.setItem(row_idx, col_idx, item)  # 테이블에 아이템 설정

        except Exception as e:
            QMessageBox.critical(self, '미리미림', '시간표 출력중 에러가 발생했습니다. 관리자에게 문의하세요.')

    def alarm_function(self, interval_seconds, icon_path):

        today = datetime.today().weekday()
        workTimes = self.my.getworkTimes()
        row = 0
        nextTimeIdx = 0
        current_time = datetime.now().time()
        notification.notify(
            title='미리미림',
            message=str(f"오늘은 {self.my.weekdays[today]}요일 입니다!"),
            app_name='미리미림 알리미',
            app_icon=icon_path,
            timeout=5
        )

        if today == 0 or today == 4:
            length = 7
        elif today == 5 or today == 6:
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
                    if "*" in next:
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