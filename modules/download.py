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
        self.package_data: dict = {}

        self.client_folder = "client"
    
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
        mods_dict = self.package_data["data"][self.now_version]["mods"]

        for mod in mods_dict:
            link = mods_dict[mod]
            file_name = f"{self.mods_path}/mods/{link.split('/')[-1]}"
            with open(file_name, "wb") as file:
                response = requests.get(link)
                file.write(response.content)
    
    def download_macos(self):
        """ 맥용 클라이언트 다운로드 및 설치 """
        # 받아야 할 클라이언트 목록
        client_dict = self.package_data["data"][self.now_version]["client"]

        for client_name in client_dict:
            download_link = client_dict[client_name]["macos"]
            file_name = f"{self.client_folder}/{download_link.split('/')[-1]}"
            with open(file_name, "wb") as file:
                response = requests.get(download_link)
                file.write(response.content)

    
    def download_windows(self):
        """ 윈도우용 클라이언트 다운로드 및 설치 """
        # 받아야 할 클라이언트 목록
        client_dict = self.package_data["data"][self.now_version]["client"]

        for client_name in client_dict:
            download_link = client_dict[client_name]["windows"]
            file_name = f"{self.client_folder}/{download_link.split('/')[-1]}"
            with open(file_name, "wb") as file:
                response = requests.get(download_link)
                file.write(response.content)

    def install_client(self):
        # 리스트 다운로드
        req = requests.get(self.package_list_link)
        self.package_data = req.json()

        # 서버에 필요한 버전
        self.now_version = self.package_data["version"]

        # 클라이언트 폴더 생성
        try:
            shutil.rmtree(self.client_folder)
        except FileNotFoundError:
            pass
        os.mkdir(self.client_folder)

        now_os = platform.system()
        if now_os == "Windows":
            self.download_windows()
        elif now_os == "Darwin":
            self.download_macos()

a = Download()
a.install_client()