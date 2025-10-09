import requests
import json
from time import sleep
from os.path import join
from os import makedirs
from openpyxl.reader.excel import load_workbook


from pprint import pprint

MAIN_ID = '1BMR4Zk3BU2Tyo7L-CYJeMfVuCxjmmT94kfz4Jp6BFAc'
MAIN_GID = 739453176
ENGLISH_ID = '1RB9AWtrYm6Y9m8NSy6On7Zk3byws8RonAGBqeneSxOo'
ENGLISH_GID = 23993546
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


def download_timetable(id, gid, timetable_filename, dest_folder=''):
    url = f'https://docs.google.com/spreadsheets/d/{id}/export'
    response = requests.get(url, params={'gid': gid})
    if dest_folder:
        makedirs(dest_folder, exist_ok=True)
    filepath = join(dest_folder, timetable_filename).replace(r'\\', '/')
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
    download_timetable(MAIN_ID, MAIN_GID, 'time.xlsx')
    print(download_timetable(ENGLISH_ID, ENGLISH_GID, 'time2.xlsx'))
    # data = get_data_from_xlsx(filepath)
    # save_json(data, OUTPUT_FILE)
    # pprint(data, sort_dicts=False)


if __name__ == '__main__':
    main()
