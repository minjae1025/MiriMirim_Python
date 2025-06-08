from MiriMirim.Program import *

def first_run():
    first_window = tk.Tk()
    first_window.title("미리미림(Miri_Mirim)")  # 프로그램 타이틀
    first_window.geometry("800x480+500+150")  # 프로그램 창 크기
    first_window.resizable(False, False)  # 창 크기 조절 막기
    first_window.mainloop()
