import requests
from time import sleep
from bs4 import BeautifulSoup as Soup

PARSING_URL = 'https://docs.google.com/spreadsheets/d/1BMR4Zk3BU2Tyo7L-CYJeMfVuCxjmmT94kfz4Jp6BFAc/edit?gid=739453176#gid=739453176'


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


def parse():
    pass

   
def main():
    pass


if __name__ == '__main__':
    parse()
