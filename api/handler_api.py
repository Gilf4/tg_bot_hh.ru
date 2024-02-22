import requests
from api.url_requests import *


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


def get_vacancies(query, page=1, per_page=10):
    params = {
        'text': query,
        'per_page': per_page,
        'page': page,
        'search_field': 'name',
        'only_with_salary': 'true'
        # 'order_by': 'publication_time' <- сортирует по дате добавления компании
    }
    data = send_requests(url_get_vacancies, params)
    return data


def get_list_of_salaries(language, level, region_named):
    params = {
        'text': f'{language} {level}',
        'per_page': 100,
        'page': 0,
        "area": region_named,
        'only_with_salary': True
    }
    salaries = []

    while True:
        response = requests.get(url_get_vacancies, params=params)
        data = response.json()
        for item in data['items']:
            salary = item['salary']
            if salary:
                from_value = salary.get('from')
                to_value = salary.get('to')
                if from_value and to_value:
                    salaries.append((from_value + to_value) / 2)
                elif from_value:
                    salaries.append(from_value)
                elif to_value:
                    salaries.append(to_value)

        if data['pages'] > params['page'] + 1:
            params['page'] += 1
        else:
            break

    return salaries


def main():
    data = get_areas_json()
    print(data)
    print(data.get('Нижний Новгород'))


if __name__ == '__main__':
    main()
