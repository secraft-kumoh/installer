import os
import shutil
import requests
import platform

def get_mods_path() -> str:
    """ 모드 폴더 경로를 반환합니다. """
    now_os = platform.system()
    mods_path: str = ""
    if now_os == "Windows":
        mods_path = os.environ["APPDATA"] + "/.minecraft"
    elif now_os == "Darwin":
        mods_path = os.environ["HOME"] + "/Library/Application Support/minecraft"
    
    return mods_path

class Download:
    def __init__(self):
        self.now_version: str = ""
        self.package_list_link: str = "https://secraft-kumoh.github.io/package/package.json"

        self.mods_path: str = get_mods_path()
    
    def mods_folder_set(self):
        """
            모드 폴더 설정
            모드 폴더가 이미 존재한다면 백업 후 폴더 생성
            백업 폴더가 존재한다면 삭제 후 기존 모드폴더를 백업
        """
        if os.path.exists(self.mods_path):
            if not os.path.exists(self.mods_path + "/mods"):
                os.mkdir(self.mods_path + "/mods")
            else:
                # 기존 백업폴더가 존재한다면 삭제
                if os.path.exists("mods"):
                    shutil.rmtree("mods")
                # 모드 폴더가 없다면 폴더를 이동
                shutil.move(self.mods_path + "/mods", "mods")

    def download_mods(self):
        """ 모드 다운로드 및 적용 """
        req = requests.get(self.package_list_link)
        data = req.json()
        # 서버에 필요한 버전
        self.now_version = data["version"]

        mods_dict = data["data"][self.now_version]["mods"]

        for mod in mods_dict:
            link = mods_dict[mod]
            file_name = f"{self.mods_path}/mods/{link.split('/')[-1]}"
            with open(file_name, "wb") as file:
                response = requests.get(link)
                file.write(response.content)
    
    def download_macos(self):
        req = requests.get(self.package_list_link)
        data = req.json()
        # 서버에 필요한 버전
        self.now_version = data["version"]

        mods_dict = data["data"][self.now_version]["mods"]

        mods_list = []
        for mod in mods_dict:
            mods_list.append(mods_dict[mod])
        
        print(mods_list)
    
a = Download()
# a.download_macos()
a.download_mods()