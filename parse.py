import requests
import json
from time import sleep
from os.path import join
from os import makedirs
from openpyxl.reader.excel import load_workbook


from pprint import pprint

PARSING_URL = 'https://docs.google.com/spreadsheets/d/1BMR4Zk3BU2Tyo7L-CYJeMfVuCxjmmT94kfz4Jp6BFAc/export'
GID = 739453176
TIMETABLE_FILENAME = 'timetable.xlsx'
DEST_FOLDER = ''
GROUP_NUMBER = 5
OUTPUT_FILE = 'schelude.json'


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


def download_timetable(gid):
    response = requests.get(PARSING_URL, params={'gid': gid})
    if DEST_FOLDER:
        makedirs(DEST_FOLDER, exist_ok=True)
    filepath = join(DEST_FOLDER, TIMETABLE_FILENAME).replace(r'\\', '/')
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def format_data(value, classnumber):
    value = value.replace('\n', '').replace('-'*21, '').replace('-'*9, '').strip()
    value = value.rsplit(' - ', maxsplit=1)
    if len(value) > 1 and classnumber:
        lecture, teacher = value
        lesson = {
            'lesson_name': lecture,
            'teacher': teacher,
            'classnumber': int(classnumber) if classnumber != '-' else 'online'
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


def get_data_from_xlsx(filepath):
    groups = ['E', 'I', 'M', 'Q', 'U', 'Y', 'AC']
    schelude = {
        'mon': [],
        'tus': [],
        'wed': [],
        'thu': [],
        'fri': [],
        'sat': [],
    }
    sheet = load_workbook(filename=filepath, data_only=True).active

    line = 11
    for key in schelude.keys():
        for _ in range(9):
            line += 1
            value = sheet[f'{groups[GROUP_NUMBER-1]}{line}'].value
            classnumber = sheet[f'{chr(ord(groups[GROUP_NUMBER-1]) + 1)}{line}'].value
            schelude[key].append(format_data(value, classnumber) if value else 'None')
    return schelude


def main():
    filepath = download_timetable(GID)
    data = get_data_from_xlsx(filepath)
    save_json(data, OUTPUT_FILE)
    pprint(data, sort_dicts=False)


if __name__ == '__main__':
    main()
