import requests
from pprint import pprint
from fake_useragent import UserAgent
import time


with open("/home/ismoilov_m_f/Python/tokens/vktoken.txt") as f:
    vk_token = f.read().split()[0]

with open("/home/ismoilov_m_f/Python/tokens/yadisk.txt") as f:
    yadisk_token = f.read().split()[0]


class Vk_class():

    def __init__(self, id=1):
        self.id = id
        self._host_vk = "https://api.vk.com/method/"
        self.dct = {}
        self.__header_vk = {"User-Agent": UserAgent().random}
        self.__params_vk = {
            "owner_id": self.id,
            "access_token": vk_token,
            "v": "5.131"
        }
        self.name_folder = time.strftime('%Y-%m-%d_%H-%M-%S')
        self._host_yan = "https://cloud-api.yandex.net"
        self.__header_yan = {"User-Agent": UserAgent().random,
                             "Content-Type": "application/json",
                             "Authorization": f"OAuth {yadisk_token}"
                             }

    def create_folder(self, name_folder: str):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.params = {"path": name_folder}
        resp = requests.put(url, params=self.params, headers=self.__header_yan)
        return resp.status_code  # 201 >>> normal

    def yan_uploader(self, img_name, img_url):

        url = f"{self._host_yan}/v1/disk/resources/upload/"
        folder_name = time.strftime('%Y-%m-%d_%H-%M-%S')

        code = self.create_folder(folder_name)
        while code != 201:
            folder_name += "(1)"
            code = self.create_folder(folder_name)

        name = img_name
        params = {
            "path": f"{folder_name}/{name}", "url": img_url, "overwrite": True}
        response = requests.post(url, params=params, headers=self.__header_yan)
        if response.status_code == 202:
            print("Completed")

    def get_photos(self):
        url = self._host_vk+"/photos.get"

        def get_resp(offset=0, count=999):
            params = {
                **self.__params_vk,
                "count": count,
                "album_id": "profile",
                "extended": "1",
                "offset": offset
                }

            response = requests.get(
                url, headers=self.__header_vk, params=params).json()["response"]
            return response

        def resp_handler(resp):
            for resp in resp["items"]:
                name_photo = f'{resp["likes"]["count"]}.jpg'
                url_photo = str(resp["sizes"][-1]["url"])
                if not name_photo in self.dct:
                    self.dct[name_photo] = url_photo
                else:
                    date = time.strftime('%Y-%m-%d_%H-%M-%S',
                                         time.localtime(resp["date"]))
                    self.dct[f'{resp["likes"]["count"]}_{date}.jpg'] = url_photo

        resp_lst = get_resp()
        count_photo = resp_lst["count"]
        offset = 999
        while count_photo > 998:
            for resp in resp_lst["items"]:
                resp_handler(resp_lst)
            resp_lst = get_resp(offset=offset, count=999)
            offset += 999
            count_photo -= offset
        else:
            if count_photo > 0.1 or offset > 998:   # если из WHILE выйдет 0
                resp_handler(resp_lst)
            else:
                print("No photos or no access to photos")
        pprint(self.dct)
        print(len(self.dct))
        print(count_photo)


#
#
#
#
#
#
"""
def create_folder(self, name_folder: str):
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    self.params = {"path": name_folder}
    resp = requests.put(url, params=self.params)
    return resp.status_code


def yan_uploader(self, img_name, img_url):

    url = f"{self._host_yan}/v1/disk/resources/upload/"
    headers = self.__header_yan
    folder_name = time.strftime('%Y-%m-%d_%H-%M-%S')
    status_code = self.create_folder(folder_name)

    name = img_name
    params = {
        "path": f"{folder_name}/{name}", "url": img_url, "overwrite": True}
    response = requests.post(url, params=params, headers=self.headers)
    if response.status_code == 202:
        print("Completed")

#
#
#
#
#
#


class YaUploader:
    def __init__(self):
        self.token = yadisk_token
        self.host = "https://cloud-api.yandex.net"
        self.headers = {"User-Agent": UserAgent().random,
                        "Content-Type": "application/json",
                        "Authorization": f"OAuth {self.token}"
                        }

    def uploader(self, path="/img1.jpg"):
        url = f"{self.host}/v1/disk/resources/upload/"
        headers = self.headers
        params = {"path": path, "url": "img_link", "overwrite": True}
        response = requests.post(url, params=params, headers=headers)
        if response.status_code == 202:
            print("Completed")
"""
