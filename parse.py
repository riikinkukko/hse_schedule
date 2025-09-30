import requests
from time import sleep
from os.path import join
from os import makedirs

PARSING_URL = 'https://docs.google.com/spreadsheets/d/1BMR4Zk3BU2Tyo7L-CYJeMfVuCxjmmT94kfz4Jp6BFAc/export?gid=739453176'
FILENAME = 'timetable.xlsx'
DEST_FOLDER = ''


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_response(url):
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            return response
        except ConnectionError:
            print('Подключение отсутствует')
            sleep(15)


def download_timetable():
    response = requests.get(PARSING_URL)
    if DEST_FOLDER:
        makedirs(DEST_FOLDER, exist_ok=True)
    filepath = join(DEST_FOLDER, FILENAME).replace(r'\\', '/')
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def main():
    pass


if __name__ == '__main__':
    download_timetable()
