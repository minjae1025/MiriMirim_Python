from plyer import notification
import time

#지정된 간격마다 알람을 울리는 함수
def alarm_function(interval_seconds, icon_path):
    while True:
        try:
            print(f"\n--- 알람: {time.strftime('%H:%M:%S')} ---")
            notification.notify(
                title='미리미림 알림',
                message=str(time.strftime('%H시 %M분 %S초입니다')),
                app_name='미리미림 알리미',
                app_icon=icon_path,
                timeout=5
            )
        except Exception as e:
            print(f"알림 실패: {e}")
        time.sleep(interval_seconds)
