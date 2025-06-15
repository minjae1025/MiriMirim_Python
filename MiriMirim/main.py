from Program import *

def programLoad():
    myInfo = myinfoLoad()
    settings = settingLoad()
    main_start(myInfo, settings)

if __name__ == "__main__":
    userInfoPath = os.path.join(bundle_dir, "source/user")
    if not os.path.isdir(userInfoPath):
        os.mkdir(userInfoPath)

    if os.path.isfile(userInfoPath + "/myInfo.json"):
        programLoad()
    else:
        first_start()
        programLoad()

