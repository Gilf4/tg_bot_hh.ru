import requests
from API.url_requests import get_vacancies_api

URL_VACANCIES = get_vacancies_api


def get_vacancies(language, page=1, per_page=10):
    params = {
        'text': f'NAME:{language}',
        'per_page': per_page,
        'page': page,
        # сортировка вакансий по дате добавления компании этой вакансии,
        # навреное надо будет выпилить потому что какие-то странные ваканции выдает
        # 'order_by': 'publication_time'
    }
    req = requests.get(URL_VACANCIES, params=params)
    if req.status_code == 200:
        return req.json()
    else:
        return None