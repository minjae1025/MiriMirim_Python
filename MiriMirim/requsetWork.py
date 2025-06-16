from fileSys import *
import datetime
from datetime import timedelta, datetime
from requestApi import requestApi

class DataWorker(QThread):
    # 2. 데이터 완료 시그널 정의 (list of lists 형태의 데이터를 전달한다고 가정)
    data_loaded = pyqtSignal(list)
    loading_finished = pyqtSignal()
    network_error = pyqtSignal()

    def __init__(self, myGrade, myClass, parent=None):
        super().__init__(parent)
        self.myGrade = myGrade
        self.myClass = myClass
        self.running = True

    def run(self):
        timeTable = [["" for _ in range(5)] for _ in range(7)]
        today = datetime.today()
        error_occurred = False

        for i in range(0, 5):
            day = today + timedelta(days=-today.weekday() + i)
            j = 0
            try:
                data = requestApi(day, self.myGrade, self.myClass)
                if data == "error":
                    # --- 수정: 오류 발생 시 시그널 방출 후 run() 종료 ---
                    self.network_error.emit()
                    error_occurred = True
                    break  # 오류 발생 시 더 이상 진행하지 않고 루프 종료
                for item in data:
                    timeTable[j][i] = item
                    j += 1
            except Exception as e:
                print(f"예외 발생: {e}")
                self.network_error.emit()
                error_occurred = True
                break

        if self.running and not error_occurred:
            print("DataWorker: 데이터 로드 성공, data_loaded 시그널 방출.")
            self.data_loaded.emit(timeTable)

        print("DataWorker: 로딩 완료, loading_finished 시그널 방출.")
        self.finished.emit()  # 로딩 완료는 항상 알림 (오류가 났든 안 났든)

    def stop(self):
        self.running = False
