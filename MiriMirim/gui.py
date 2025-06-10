import sys

from PyQt5.QtCore import QCoreApplication
from fileSys import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#UI파일 연결
firstUi = uic.loadUiType("../gui/firstWindow.ui")[0]

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



def first_start():
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    firstWindow = firstWindowClass()
    firstWindow.startBtn.clicked.connect(firstWindow.start)

    #프로그램 화면을 보여주는 코드
    firstWindow.show()

    #프로그램을 이벤트루프로 진입시키는 코드
    app.exec()