from fileSys import *
tray_icon = None

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
            QMessageBox.warning(self, '미리미림', '학년과 반을 선택해 주세요')
            return

        myinfoSave(userName, userGrade, userClass)
        self.close()

    def closeEvent(self, closeEvent):
        reply = QMessageBox.question(self, '미리미림',
                                     "정말 프로그램을 종료하시겠습니까?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
           closeEvent.accept() # 이벤트를 수락하여 종료를 진행
           sys.exit(0) # 애플리케이션 종료 (성공 코드 0)
        else:
           closeEvent.ignore() # 이벤트를 무시하여 종료를 취소
