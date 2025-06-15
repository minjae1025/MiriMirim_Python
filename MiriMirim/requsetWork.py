from fileSys import *
import datetime
from datetime import timedelta, datetime
from requestApi import requestApi

class DataWorker(QThread):
    # 2. 데이터 완료 시그널 정의 (list of lists 형태의 데이터를 전달한다고 가정)
    data_loaded = pyqtSignal(list)
    loading_finished = pyqtSignal() # 로딩 완료를 알리는 시그널 (데이터가 없을 때)

    def __init__(self, myGrade, myClass, parent=None):
        super().__init__(parent)
        self.myGrade = myGrade
        self.myClass = myClass
        self.running = True

    def run(self):
        timeTable = [["" for _ in range(5)] for _ in range(7)]
        today = datetime.today()
        for i in range(0, 5):
            day = today + timedelta(days=-today.weekday() + i)
            j = 0
            try:
                data = requestApi(day, self.myGrade, self.myClass)
                if data == "error":
                    retry = QMessageBox.critical(self, '인터넷 오류!', '인터넷이 오류로 인한 프로그램 실행에 실패했습니다. 재시도 하시겠습니까?',
                                                 QMessageBox.YES | QMessageBox.NO)
                    if retry == QMessageBox.Yes:
                        return False
                for item in data:
                    timeTable[j][i] = item
                    j += 1
            except Exception as e:
                print(e)

        if self.running: # 스레드가 종료되지 않았을 경우에만 시그널 방출
            self.data_loaded.emit(timeTable) # 데이터와 함께 시그널 방출
            self.loading_finished.emit() # 로딩 완료 시그널 방출

    def stop(self):
        self.running = False
        self.wait() # 스레드 종료를 기다림