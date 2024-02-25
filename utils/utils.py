from collections import defaultdict
from api.handler_api import get_areas_json, get_vacancies, send_requests
from utils.formats import format_vacancies, format_skills
import statistics


def json_areas_to_dict(areas_json: any, areas: dict) -> None:
    """
    Функциа рекурсивного парсинка json'а мест
    :param areas_json: json мест
    :param areas: Словарь куда будут складываться найденные значения
    """

    for area in areas_json:
        areas[area['name']] = area['id']

        if area.get('areas'):
            json_areas_to_dict(area['areas'], areas)


def get_areas() -> dict:
    """
    :return: Cловарь мест в виде {area_lower: number} и {number: area}. Где number - индефикатор места
    """

    areas_tree = get_areas_json()
    areas = {}
    json_areas_to_dict(areas_tree, areas)

    for name in list(areas):
        areas[name.lower()] = areas[name]
        areas[areas[name]] = name

    return areas


def smarted_get_vacancies(query: str, count_vacancies: int = 0, area: str = None) -> list:
    """
    Функция возвращает n - ое количество вакансий или максимум вакансий, который есть (может быть [ ]).
    :param query: Запрос по вакансий (python developer, уборщик пятёрочки)
    :param count_vacancies: Количестов запрашиваемых вакансий. Если нужны все, то можно ничего не указывать или указать 0
    :param area: Не реализована
    :return: Список вакансий
    """

    page = -1  # Сдвиг для красоты (первая страница - 0)
    data = []  # Список вакансий

    while len(data) < count_vacancies or not count_vacancies:
        page += 1
        vacancies = get_vacancies(query, page=page, per_page=100)

        if vacancies and vacancies['items']:
            data.extend(vacancies['items'])
        else:
            break

        if page == vacancies.get('pages'):  # Проверка на последнюю стнаницу
            break

    if count_vacancies:
        data = data[:count_vacancies]  # Срезаем лишнии вакансии

    return data


def get_count_vacancies(query: str, area: str = None) -> int:
    """
    :param query: Запрос по вакансий (python developer, уборщик пятёрочки)
    :param area: Место поиска вакансий
    :return: Количество найденных вакансий
    """

    data = get_vacancies(query)
    return data.get('found', 0)


def extend_vacancies(list_vacancies: list) -> list:
    """
    Функция расширяет информацию о вакансиях. Работает очень медлено, 1 - 4 с. одна вакансия!
    :param list_vacancies: список вакансий для расширения. Предпочтительнее, взятых из smarted_get_vacancies
    :return: список расширенных вакансий
    """

    data = []

    for vacancy in list_vacancies:
        url = vacancy.get('url')  # Получение ссылки на данные со страницы вакансии

        if url:
            vacancy = send_requests(url)
        else:
            continue

        if vacancy:
            data.append(vacancy)

    return data


def get_skills(extended_vacancies: list) -> dict:
    """
    :param extended_vacancies: Список расширенных вакансий
    :return: Словарь вида {name_skill: count}, где count - количество вакансий с таким скиллом
    """

    skills = defaultdict(int)

    for vacancy in extended_vacancies:
        for skill in vacancy.get('key_skills', []):
            skills[skill['name']] += 1

    return skills


def get_format_skills(query: str) -> str:
    """
    Функция для получения форматированного сообщения о стеке технологий по запросу. Работает медлено!
    :param query: Запрос
    :return: Форматированное сообщение о стеке технологий
    """

    data = smarted_get_vacancies(query)[:40]
    extended_data = extend_vacancies(data)
    skills = get_skills(extended_data)
    message = format_skills(skills, len(extended_data))
    return message


def get_format_vacancies(text):
    vacancies = smarted_get_vacancies(text, count_vacancies=10)
    return format_vacancies(vacancies)


def calculate_average_salary(list_of_salaries):
    return statistics.median(list_of_salaries)


def sort_by_price_vacancies(list_vacancies: list, key_sort: any, reverse=True) -> list:
    """
    Функция сортирукт вакансии по параметру, который задаётся ключём сортировки (костыль 1 - ый,
    - сортировка уже полученных данных, а не сортировка при запросе данных).
    Вакансии с зарплатами в других волютах убираються (костыль 2 - ой, - отсутствие конвертации валюты)
    :param list_vacancies: Список вакансий для сортировка
    :param key_sort: Функция, указывающая, параметр по которому будет производиться сортировка
    :param reverse: Если True - сортирует по не возрастанию (включено по дефолту). Если False - по не убыванию
    :return: Новый отсортированный список
    """

    list_vacancies_ru = []

    for i in range(len(list_vacancies)):  # Костыль для других волют
        if list_vacancies[i]['salary']['currency'] == 'RUR':
            list_vacancies_ru.append(list_vacancies[i])

    list_vacancies_ru.sort(key=key_sort, reverse=reverse)

    return list_vacancies_ru


def get_experience() -> dict:
    """
    :return: Словарь вида {name_experience: id_experience}
    """

    return {'Нет опыта': 'noExperience',
            'От 1 года до 3 лет': 'between1And3',
            'От 3 до 6 лет': 'between3And6',
            'Более 6 лет': 'moreThan6'}


def main():
    data = smarted_get_vacancies('Уборщик')
    data = sort_by_price_vacancies(data)
    for el in data:
        print(el['alternate_url'])
        print(el['salary']['from'], el['salary']['to'])


if __name__ == '__main__':
    main()
