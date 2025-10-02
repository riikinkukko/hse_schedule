import requests
import openpyxl
import json
from time import sleep
from os.path import join
from os import makedirs
from openpyxl.reader.excel import load_workbook

from pprint import pprint

PARSING_URL = 'https://docs.google.com/spreadsheets/d/1BMR4Zk3BU2Tyo7L-CYJeMfVuCxjmmT94kfz4Jp6BFAc/export?gid=739453176'
FILENAME = 'timetable.xlsx'
DEST_FOLDER = ''
GROUP_NUMBER = 5
JSON_FILE = 'schelude.json'


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


def render_data(value, classnumber):
    trash = ['---------------------', '---------']
    value = value.replace('\n', '').replace(trash[0], '').replace(trash[1], '').strip()
    value = value.rsplit(' - ', maxsplit=1)
    if len(value) > 1 and classnumber:
        lecture, teacher = value
        lesson = {
            'lesson_name': lecture,
            'teacher': teacher,
            'classnumber': int(classnumber) if classnumber != '-' else '-'
        }
        return lesson
    return 'None'


def save_json(data, filename, folder=''):
    if folder:
        makedirs(folder, exist_ok=True)
    filepath = join(folder, filename)
    with open(filepath, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False)
    return filepath


def get_data_from_xlsx():
    groups = ['E', 'I', 'M', 'Q', 'U', 'Y', 'AC']
    schelude = {
        'mon': [],
        'tus': [],
        'wed': [],
        'thu': [],
        'fri': [],
        'sat': [],
        'sun': [],
    }
    sheet = load_workbook(filename=FILENAME, data_only=True).active

    count = 11
    for key in schelude.keys():
        for _ in range(9):
            count += 1
            value = sheet[f'{groups[GROUP_NUMBER-1]}{count}'].value
            classnumber = sheet[f'{'V'}{count}'].value
            schelude[key].append(render_data(value, classnumber) if value else 'None')
    save_json(schelude, JSON_FILE)
    pprint(schelude, sort_dicts=False)


def main():
    pass


if __name__ == '__main__':
    get_data_from_xlsx()
