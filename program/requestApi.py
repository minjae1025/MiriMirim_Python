import datetime, requests, json

today = datetime.date.today()
API_KEY = "90de860d4ab54f7eb75640bf431149a4"
URL = "https://open.neis.go.kr/hub/hisTimetable?"
ATPT_OFCDC_SC_CODE = "B10"
SD_SCHUL_CODE = "7011569"
TYPE = "json"
GRADE = 2 #임시값
CLASS_NM = 4 #임시값
ALL_TI_YMD = today.strftime("%Y%m%d")

def requestApi():
    AY = str(today.year)
    SEM = ""
    if (today.month < 3 or today.month > 7):
        SEM = "2"
    else:
        SEM = "1"

    api_url = "https://open.neis.go.kr/hub/hisTimetable?KEY=" + API_KEY + "&ATPT_OFCDC_SC_CODE=" + ATPT_OFCDC_SC_CODE + "&SD_SCHUL_CODE=" + SD_SCHUL_CODE + "&AY=" + AY + "&SEM=" + SEM + "&ALL_TI_YMD=" + ALL_TI_YMD + "&GRADE=" + str(
        GRADE) + "&CLASS_NM=" + str(CLASS_NM) + "&Type=" + TYPE
    request = requests.get(api_url)
    data = request.json()
    data = data['hisTimetable'][1]['row']
    subjects = []
    for item in data:
        temp = json.dumps(item["ITRT_CNTNT"])
        subjects.append(temp.encode("utf8").decode('unicode_escape'))
    return subjects

# data = requestApi()
# print(today.strftime("%Y년 %m월 %d일")+" 시간표")
# for item in data:
#     test = json.dumps(item["ITRT_CNTNT"])
#     print(test.encode("utf8").decode('unicode_escape'))

