import requests
from url_requests import *


def send_requests(url: str, par: dict = None) -> any:
    """
    :param url: url api
    :param par: options params
    :return: json request for url with params
    """

    req = requests.get(url, params=par)

    if req.status_code == 200:
        data = req.json()
        req.close()
        return data


def get_areas_json() -> any:
    """
    :return: returned json areas
    """

    return send_requests(url_get_areas)


def get_vacancies(language, page=1, per_page=10):
    params = {
        'text': f'NAME:{language}',
        'per_page': per_page,
        'page': page,
        # 'order_by': 'publication_time' <- сортирует по дате добавления компании
    }
    req = requests.get(url_get_vacancies, params=params)
    if req.status_code == 200:
        return req.json()
    else:
        return None


def main():
    data = get_areas_json(True)
    print(data)
    print(data.get('Нижний Новгород'))


if __name__ == '__main__':
    main()
