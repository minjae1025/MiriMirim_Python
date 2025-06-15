from Program import *

def programLoad():
    myInfo = myinfoLoad()
    settings = settingLoad()
    main_start(myInfo, settings)

if __name__ == "__main__":
    userPath = os.path.join(bundle_dir, "source/user")
    if not os.path.isdir(userPath):
        os.mkdir(userPath)

    userInfoPath = os.path.join(bundle_dir, "source/user/myInfo.json")

    if os.path.exists(userInfoPath):
        programLoad()

    else:
        is_setup_successful = first_start()  # first_start가 성공 여부를 반환한다고 가정
        if is_setup_successful:
            programLoad()
        else:
            print("초기 설정이 완료되지 않았습니다. 프로그램을 종료합니다.")
            sys.exit()

