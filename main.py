from pprint import pprint

import requests

# ЗАДАНИЕ №1

heroes_dict = {'heroes': ['Hulk', 'Captain America', 'Thanos']}
names_list = []
intelligence_list = []


def most_intelligent_hero():
    for names in heroes_dict.values():
        for name in names:
            url = f'https://superheroapi.com/api/2619421814940190/search/{name}'
            hero_description = requests.get(url).json()
            results = hero_description.get('results')
            for result in results:
                name = result.get('name')
                names_list.append(name)
                powerstats = result.get('powerstats')
                intelligence = int(powerstats.get('intelligence'))
                intelligence_list.append(intelligence)
                zipped = list(zip(names_list, intelligence_list))
                zipped.sort(key = lambda tup: tup[1], reverse = True)
        return f'Самый умный герой: {zipped[0]}'

print(most_intelligent_hero())

# ЗАДАНИЕ №2

# TOKEN = 'здесь пишем свой токен'


class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        """Метод получает ссылку, по которой далее загружается файл на яндекс диск"""
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, disk_file_path, filename):
        """Метод загруджает файл file_path на яндекс диск"""
        href = self._get_upload_link(disk_file_path=disk_file_path).get('href', '')
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Success')


if __name__ == '__main__':
    uploader = YaUploader(token=TOKEN)
    pprint(uploader.upload('Netology/Test.txt', 'Test.txt'))