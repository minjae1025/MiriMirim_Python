import datetime
from program.requestApi import requestApi
from program.systemTray import *
import time

def setup_tray_icon():
    #시스템 트레이 아이콘을 설정하고 시작하는 함수
    # try:
    #     image = Image.open("./img/miri_mirim.png")
    # except FileNotFoundError:
    #     image = Image.new('RGB', (64, 64), color='white')
    image = Image.open(image_path)

    tray_icon = pystray.Icon(
        'miri_mirim', image, '미리미림',
        menu=pystray.Menu(
            pystray.MenuItem('창 열기', show_window, default=True),
            pystray.MenuItem('숨기기', hide_window),
            pystray.MenuItem('종료', quit_application)
        )
    )
    # 아이콘을 백그라운드 스레드에서 실행
    tray_icon.run() #블록킹 함수. 별도 스레드에서 실행


def main_program():
    today = datetime.date.today()
    titleLabel = tk.Label(root_window, text=str(today.strftime("%Y년 %m월 %d일") + " 시간표"))
    titleLabel.pack()

    try:
        data = requestApi()
        for item in data:
            label = tk.Label(root_window, text=str(item))
            label.pack()
    except Exception as e:
        tk.Label(root_window, text=f"API 데이터 로딩 오류: {e}").pack()


    # 윈도우 닫기 버튼(X) 클릭 시 on_closing 함수 호출
    root_window.protocol("WM_DELETE_WINDOW", on_closing)
    root_window.mainloop()

