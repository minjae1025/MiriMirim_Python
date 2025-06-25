import requests, json, os
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
from dotenv import load_dotenv

load_dotenv()
today = datetime.today()
API_KEY = os.environ.get("API_KEY")
URL = "https://open.neis.go.kr/hub/hisTimetable?"
ATPT_OFCDC_SC_CODE = "B10"
SD_SCHUL_CODE = "7011569"
TYPE = "json"
AY = str(today.year)
SEM = ""
majorSubjects = ['프로그래밍', '컴퓨터', '웹사이트', '네트워크', '서버', '데이터베이스', 'SQL', 'UI', '디자인', '광고', '그래픽', 'CG',
                                 '색채', '비주얼', 'UX', '콘텐츠']


def requestApi(ALL_TI_YMD, GRADE, CLASS_NM):
    day = ALL_TI_YMD
    ALL_TI_YMD = ALL_TI_YMD.strftime("%Y%m%d")
    if (today.month < 3 or today.month > 7):
        SEM = "2"
    else:
        SEM = "1"
    api_url = (URL+"KEY="+API_KEY+"&ATPT_OFCDC_SC_CODE="+ATPT_OFCDC_SC_CODE+"&SD_SCHUL_CODE="+SD_SCHUL_CODE+"&AY="+AY+"&SEM="+SEM+"&ALL_TI_YMD="+ALL_TI_YMD+"&GRADE="+
               str(GRADE)+"&CLASS_NM="+str(CLASS_NM)+"&Type="+TYPE)
    subjects = []
    print(api_url)
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        data = data["hisTimetable"][1]['row']
        i = 1
        for item in data:
            if GRADE == '2' and day.weekday() == 4 and (i == 5 or i == 6):
                temp = "선택 과목"
            else:
                temp = json.dumps(item["ITRT_CNTNT"]).encode("utf8").decode('unicode_escape')[1:-1]
                if any(sub_string in temp for sub_string in majorSubjects):
                    if not '*' in temp:
                        temp = '* '+temp

            subjects.append(temp)
            i+=1
    except:
        return "error"

    return subjects