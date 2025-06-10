import pystray, sys, os, tkinter as tk
from datetime import datetime, timedelta
from PIL import Image
from monitorInfo import *
from MiriMirim.requestApi import requestApi
from MiriMirim.Account import Account
tray_icon = None

class Program:
    def __init__(self, myInfo):
        self.my = Account(myInfo)
        self.root_window = tk.Tk()
        self.root_window.title("미리미림(Miri_Mirim)")  # 프로그램 타이틀
        #self.root_window.geometry(resolution+"+500+150")  # 프로그램 창 크기
        self.root_window.geometry("1600x900+500+150")
        self.root_window.resizable(False, False)
        self.root_window.protocol("WM_DELETE_WINDOW", self.on_closing)


    def show_window(self):
        # 윈도우를 다시 보여주는 함수
        if self.root_window:
            print("창을 표시합니다.")
            self.root_window.deiconify()  # 창을 다시 표시
            self.root_window.focus_force()  # 창에 포커스 주기

    def hide_window(self):
        # 윈도우를 숨기는 함수
        if self.root_window:
            print("창을 숨깁니다.")
            self.root_window.withdraw()  # 창을 숨김 (최소화와 다름)

    def quit_application(self):
        # 애플리케이션을 종료하는 함수
        if self.root_window:
            self.root_window.quit()  # Tkinter 메인 루프 종료
            self.root_window.destroy()  # Tkinter 윈도우 파괴
        if tray_icon:
            tray_icon.stop()  # pystray 아이콘 루프 종료
        print("프로그램이 완전히 종료되었습니다.")

    def on_closing(self):
        self.hide_window()  # 창을 숨김

    def setup(self):
        tray_icon = pystray.Icon(
            'miri_mirim', image, '미리미림',
            menu=pystray.Menu(
                pystray.MenuItem('창 열기', self.show_window, default=True),
                pystray.MenuItem('숨기기', self.hide_window),
                pystray.MenuItem('종료', self.quit_application)
            )
        )
        # 아이콘을 백그라운드 스레드에서 실행
        tray_icon.run()

    def main_program(self):
        frame = tk.Frame(self.root_window, width=width, height=height)
        today = datetime.today()
        titleLabel = tk.Label(frame, text=(str(self.my.myGrade)+"학년 "+str(self.my.myClass)+"반 시간표"))
        titleLabel.pack()

        for i in range(0, 5):
            day = today + timedelta(days=-today.weekday()+i)
            j = 0
            try:
                data = requestApi(day.strftime("%Y%m%d"), self.my.myGrade, self.my.myClass)
                for item in data:
                    self.my.Timetable[i][j] = item
                    label = tk.Label(frame, text=str(item))
                    label.pack()
                    j += 1
            except Exception as e:
                print(e)
                tk.Label(frame, text=f"API 데이터 로딩 오류: {e}").pack()

        frame.pack()
        self.root_window.mainloop()
        # for i in range(len(self.my.Timetable)):
        #     for j in range(len(self.my.Timetable[i])):
        #         print(self.my.Timetable[i][j])





if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.abspath(os.path.dirname(__file__))

image_path = os.path.join(bundle_dir, '../img', 'miri_mirim.ico')
icon_image = Image.open(image_path)
notification_icon_path = image_path
image = Image.open(image_path)





