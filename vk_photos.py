from fake_useragent import UserAgent
from pprint import pprint
from tqdm import tqdm
import requests
import json
import time
with open("vktoken.txt") as f:
    vk_token = f.readline().strip()
with open("yadisk.txt") as f:
    yadisk_token = f.readline().strip()


class Vk_class():
    def __init__(self, id=1, count=5, album="profile"):
        self.id = id
        self.album = album
        self._host_vk = "https://api.vk.com/method/"
        self.lst = []
        self.count = count
        self.__header_vk = {"User-Agent": UserAgent().random}
        self.__params_vk = {
            "owner_id": self.id,
            "access_token": vk_token,
            "v": "5.131"
        }
        self.file_name = "VK_requiremеnts.json"
        self.name_folder = "VK " + time.strftime('%Y-%m-%d_%H-%M-%S')
        self._host_yan = "https://cloud-api.yandex.net"
        self.__header_yan = {"User-Agent": UserAgent().random,
                             "Content-Type": "application/json",
                             "Authorization": f"OAuth {yadisk_token}"
                             }
        self.name_folder = self.__create_folder(self.name_folder)
        with open("requirements.txt", "w") as req:
            req.write("fake_useragent\n")
            req.write("requests\n")
            req.write("tqdm\n")
            req.write("json")
        with open(self.file_name, "w") as f:
            f.write("[{\n}]")

    def __create_folder(self, name_folder: str):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.params = {"path": name_folder}
        resp = requests.put(url, params=self.params, headers=self.__header_yan)
        if resp.status_code == 201:
            return name_folder
        else:
            time.sleep(1)
            self.__create_folder(
                self.name_folder+time.strftime('%Y-%m-%d_%H-%M-%S'))

    def _yan_uploader(self, name_portal, img_name, img_url):
        url = f"{self._host_yan}/v1/disk/resources/upload/"
        name = img_name
        params = {
            "path": f"{self.name_folder}/{name}", "url": img_url, "overwrite": True}
        response = requests.post(url, params=params, headers=self.__header_yan)

    def __get_resp(self, offset=0):
        url = self._host_vk+"/photos.get"
        params = {
            **self.__params_vk,
            "count": self.count,
            "album_id": self.album,
            "extended": "1",
            "offset": offset
            }
        response = requests.get(
            url, headers=self.__header_vk, params=params).json()
        if "error" in response:
            return
        else:
            return response["response"]

    def __resp_handler(self, resp):
        self.list_names = []
        for resp in tqdm(resp["items"], desc=("Download"), unit=" img", disable=False):
            name_photo = f'{resp["likes"]["count"]}.jpg'
            url_photo = str(resp["sizes"][-1]["url"])
            size = {'width': resp["sizes"][-1]['width'],
                    'height': resp["sizes"][-1]['height']}
            if not name_photo in self.list_names:
                self.lst.append({"file_name": name_photo, "sizes": size})
                self.list_names.append(name_photo)
            else:
                date = time.strftime('%Y-%m-%d_%H-%M-%S',
                                     time.localtime(resp["date"]))
                self.lst.append(
                    {"file_name": name_photo+"_"+date, "sizes": size})
                self.list_names.append(name_photo+"_"+date)
            self._yan_uploader("VK", name_photo, url_photo)

            # print(size)
            # time.sleep(0.1)
        with open(self.file_name, "w") as f:
            json.dump(self.lst, f, indent=1)
        del self.list_names

    def get_photos(self):
        url = self._host_vk+"/photos.get"
        resp_lst = self.__get_resp()
        if not resp_lst:
            print(
                "Передали неверные данные(API, ID, Album_id) или нет доступа к фотографиям")
        else:
            count_photo = resp_lst["count"]
        offset = 999
        while count_photo > 998:
            self.__resp_handler(resp_lst)
            resp_lst = self.__get_resp(offset=offset)
            offset += 999
            count_photo -= offset
        else:
            if count_photo > 0.1 or offset > 998:   # если из WHILE выйдет 0
                self.__resp_handler(resp_lst)
        # pprint(self.lst)
        # print(len(self.lst))
        # print(count_photo)
        print(
            f"Загружено {len(self.lst)} фотографии из {count_photo}, на папку: {self.name_folder}")
