import pystray
from PIL import Image
import tkinter as tk
from monitorInfo import *
import os
import sys
tray_icon = None

def show_window():
    #윈도우를 다시 보여주는 함수
    if root_window:
        print("창을 표시합니다.")
        root_window.deiconify() # 창을 다시 표시
        root_window.focus_force() # 창에 포커스 주기

def hide_window():
    #윈도우를 숨기는 함수
    if root_window:
        print("창을 숨깁니다.")
        root_window.withdraw() # 창을 숨김 (최소화와 다름)

def quit_application():
    #애플리케이션을 종료하는 함수
    if root_window:
        root_window.quit() # Tkinter 메인 루프 종료
        root_window.destroy() # Tkinter 윈도우 파괴
    if tray_icon:
        tray_icon.stop() # pystray 아이콘 루프 종료
    print("프로그램이 완전히 종료되었습니다.")
    # 필요한 경우 모든 스레드를 안전하게 종료하는 로직 추가 (daemon=True면 자동으로 종료)


def on_closing():
    hide_window() # 창을 숨김

root_window = tk.Tk()
root_window.title("미리미림(Miri_Mirim)")  # 프로그램 타이틀
root_window.geometry(str(int(width / 1.5)) + "x" + str(int(height / 1.5)) + "+500+150")  # 프로그램 창 크기
root_window.resizable(False, False)  # 창 크기 조절 막기

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.abspath(os.path.dirname(__file__))

image_path = os.path.join(bundle_dir, '../img', 'miri_mirim.ico')
icon_image = Image.open(image_path)
notification_icon_path = image_path



