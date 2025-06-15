from fileSys import *
tray_icon = None

#화면을 띄우는데 사용되는 Class 선언
class firstWindowClass(QDialog, firstUi) :
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
        self.accept()

    def closeEvent(self, closeEvent):
        reply = QMessageBox.question(self, '미리미림',
                                     "정말 종료하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            closeEvent.accept()  # 종료 이벤트 수락
            # QDialog의 경우, reject()를 호출하여 exec()가 QDialog.Rejected를 반환하도록 함
            self.reject()
        else:
            closeEvent.ignore()
