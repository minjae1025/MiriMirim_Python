from gui import *

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

def main_start(myInfo):
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  #마지막 윈도우가 닫혀도 앱 종료 안 함 (트레이 유지)
    mainWindow = MainWindowClass(myInfo)
    mainWindow.show()  # 메인 윈도우 표시
    mainWindow.setup_tray_icon()
    mainWindow.main_program()

    app.exec()



