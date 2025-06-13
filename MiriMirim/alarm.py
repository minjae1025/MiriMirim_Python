from plyer import notification
import time
from datetime import datetime

from pyexpat.errors import messages


#지정된 간격마다 알람을 울리는 함수
def alarm_function(interval_seconds, icon_path, my):
    today = datetime.today().weekday()
    workTimes = my.getworkTimes()
    row = 0
    nextTimeIdx = 0
    current_time = datetime.now().time()
    if today == 0 or today == 4:
        length = 6
    elif today == 5 or today == 6:
        notification.notify(
            title='미리미림',
            message=str(f"오늘은 주말입니다!"),
            app_name='미리미림 알리미',
            app_icon=icon_path,
            timeout=5
        )
        return
    else:
        length = 7

    for item in workTimes:
        if datetime.strptime(item, "%H:%M").time() < current_time:
            nextTimeIdx += 1
            row += 1

    while True:
        today = datetime.today().weekday()
        column = today

        if nextTimeIdx == length:
            continue
        current_time = datetime.now().time()
        parsed_time = datetime.strptime(workTimes[nextTimeIdx], "%H:%M").time()

        # print(parsed_time)
        # print(workTimes[nextTimeIdx])
        print(current_time)

        if current_time>parsed_time:
            next = my.timeTable[row][column]
            if "*" in next:
                subject = f"전공 수업인 {next}"
            else:
                subject = f"{next}"
            try:
                if nextTimeIdx == 4:
                    message = "곧 점심시간입니다!"
                else:
                    message = f"다음 교시는 {subject}입니다. 미리 준비하세요!"
                    row += 1

                notification.notify(
                    title='미리미림',
                    message=message,
                    app_name='미리미림 알리미',
                    app_icon=icon_path,
                    timeout=5
                )
                nextTimeIdx += 1
            except Exception as e:
                print(f"알림 실패: {e} ")

        current_time = datetime.now().time()
        time.sleep(interval_seconds)
