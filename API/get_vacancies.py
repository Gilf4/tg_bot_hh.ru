import requests


URL_VACANCIES = 'https://api.hh.ru/vacancies'


def get_vacancies(language, page=0, per_page=10):
    params = {
        'text': f'NAME:{language}',
        'per_page': per_page,
        'page': page,
        # сортировка вакансий по дате добавления компании этой вакансии,
        # навреное надо будет выпилить потому что какие-то странные ваканции выдает
        #'order_by': 'publication_time'
    }
    req = requests.get(URL_VACANCIES, params=params)
    if req.status_code == 200:
        return req.json()
    else:
        return None
