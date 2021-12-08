import requests
import json
import os
import time
from tqdm import tqdm, tqdm_gui, trange
from pprint import pprint

os.chdir(r'D:\test\Netology\diplom_osnovy')


class VkUser:

    url = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.params = {
            'access_token': token,
            'v': '5.131'
        }

    def get_photo_info(self, owner_id):

        get_photo_url = self.url + 'photos.get'

        get_photo_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': '1'
        }

        data = {}
        res = requests.get(get_photo_url, params={**self.params, **get_photo_params})
        info = res.json()
        with open('data.json', 'w') as f:
            json.dump(info, f)
        data.update(res.json())
        data_dict = {}
        data_list = []
        res_dict = {}
        res_list = []
        for i in range(len(data['response']['items'])):
            name = data['response']['items'][i]['likes']['count']
            size = data['response']['items'][i]['sizes'][-1]['type']
            url = data['response']['items'][i]['sizes'][-1]['url']
            res_dict = ({'file_name': str(name) + '.jpg', 'size': size, 'url': url})
            res_list.append(res_dict)

        return res_list


class YaUploader:

    url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return{
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self):
        create_url = self.url + 'resources'
        params = {'path': f'Photo id {str(id)}'}
        response = requests.put(url=create_url, headers=self.get_headers(), params=params)
        if response.status_code == 201:
            print("Папка создана.")
        return f'Photo id {str(id)}'

    def upload_link(self, data_list):
        upload_url = self.url + 'resources/upload'
        headers = self.get_headers()
        for i in trange(len(data_list)):
            file_name = data_list[i]['file_name']
            url = data_list[i]['url']
            params = {'path': f'{path}/{file_name}', 'url': url, 'disable_redirects': False}
            response = requests.post(url=upload_url, headers=headers, params=params)
            time.sleep(5)
            response.raise_for_status()
            if response.status_code == 201:
                print('Загрузка прошла успешно.')

# result = VkUser(token)

# result_file = result.get_photo_info('95943317')

# pprint(result_file)


with open('vk_token.txt', 'r') as file:
    token = file.read().strip()

if __name__ == '__main__':
    id = int(input('Пожалуйста, введите id пользователя Vk:'))
    token_YaDisk = str(input('Также введите токен с Полигона Яндекс.Диска:'))
    data_photo = VkUser(token)
    uploader = YaUploader(token_YaDisk)
    path = uploader.create_folder()
    result = data_photo.get_photo_info(id)
    final_result = uploader.upload_link(result)




# pprint(VkUser.get_photo_info('95943317'))


