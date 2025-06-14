import requests, json
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox

today = datetime.today()
API_KEY = "90de860d4ab54f7eb75640bf431149a4"
URL = "https://open.neis.go.kr/hub/hisTimetable?"
ATPT_OFCDC_SC_CODE = "B10"
SD_SCHUL_CODE = "7011569"
TYPE = "json"
AY = str(today.year)
SEM = ""


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
    try:
        response = requests.get(api_url, timeout=3)
        data = response.json()
        print(api_url)
        data = data["hisTimetable"][1]['row']
        i = 1
        for item in data:
            if day.weekday() == 4 and (i == 5 or i == 6):
                temp = "'선택 과목'"
            else:
                temp = json.dumps(item["ITRT_CNTNT"]).encode("utf8").decode('unicode_escape')
            subjects.append(temp)
            i+=1
    except:
        return "error"

    return subjects