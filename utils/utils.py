from collections import defaultdict
from api.handler_api import get_areas_json, get_vacancies, send_requests
from utils.formats import format_vacancies, format_skills
from utils.keys_sort import sort_by_salaries
from utils.filters import FilterPresenceSalary, FilterCurrency
from utils.params_get_vacancies import Params
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


def smarted_get_vacancies(params: dict, count_vacancies: int = 0) -> list:
    """
    Функция возвращает n - ое количество вакансий или максимум вакансий, который есть (может быть [ ]).
    :param count_vacancies: Количестов запрашиваемых вакансий. Если нужны все, то можно ничего не указывать или указать 0
    :param params: Параметры для получения вакансии в виде словаря. Для приготовленя рекомундуеться params_get_vacancies
    :return: Список вакансий
    """

    page = -1  # Сдвиг для красоты (первая страница - 0)
    data = []  # Список вакансий
    params[Params.key_per_page] = 100  # Устоновка максимального количество получаемых вакансий

    while len(data) < count_vacancies or not count_vacancies:
        page += 1
        params[Params.key_page] = page
        vacancies = get_vacancies(params)

        if vacancies and vacancies['items']:
            data.extend(vacancies['items'])
        else:
            break

        if page == vacancies.get('pages'):  # Проверка на последнюю стнаницу
            break

    if count_vacancies:
        data = data[:count_vacancies]  # Срезаем лишнии вакансии

    return data


def get_count_vacancies(params: dict) -> int:
    """
    :param params: Параметры для получения вакансии в виде словаря. Для приготовленя рекомундуеться params_get_vacancies
    :return: Количество найденных вакансий
    """

    data = get_vacancies(params)
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


def get_format_skills(params: dict) -> str:
    """
    Функция для получения форматированного сообщения о стеке технологий по запросу. Работает медлено!
    :param params: Параметры для получения вакансии в виде словаря. Для приготовленя рекомундуеться params_get_vacancies
    :return: Форматированное сообщение о стеке технологий
    """

    data = smarted_get_vacancies(params)[:40]
    extended_data = extend_vacancies(data)
    skills = get_skills(extended_data)
    message = format_skills(skills, len(extended_data))
    return message


def get_format_vacancies(params: dict):
    """
    :param params: Параметры для получения вакансии в виде словаря. Для приготовленя рекомундуеться params_get_vacancies
    :return:
    """

    vacancies = smarted_get_vacancies(params, count_vacancies=10)
    return format_vacancies(vacancies)


def calculate_average_salary(list_of_salaries):
    return statistics.median(list_of_salaries)


def custom_sort_vacancies(vacancies: list, key_sort: any, reverse=True) -> list:
    """
    Функция сортирукт вакансии по параметру, который задаётся ключём сортировки (костыль 1 - ый,
    - сортировка уже полученных данных, а не сортировка при запросе данных).
    Вакансии с зарплатами в других волютах убираються (костыль 2 - ой, - отсутствие конвертации валюты)
    :param vacancies: Список вакансий для сортировка
    :param key_sort: Функция, указывающая, параметр по которому будет производиться сортировка
    :param reverse: Если True - сортирует по не возрастанию (включено по дефолту). Если False - по не убыванию
    :return: Новый отсортированный список
    """

    vacancies_ru = custom_filter_vacancies(vacancies, FilterCurrency('RUR'))

    vacancies_ru.sort(key=key_sort, reverse=reverse)

    return vacancies_ru


def custom_filter_vacancies(vacancies: list, *args) -> list:
    """
    Функция для фильтрации вакансий
    :param vacancies: вакансии для вильтрации
    :param args: совокупность фильтров для вакансий, переданных через запятую
    :return: отфильтрованый список
    """

    filtered_vacancies = []

    for vacancy in vacancies:
        for my_filter in args:
            if not my_filter.is_(vacancy):
                break
        else:
            filtered_vacancies.append(vacancy)

    return filtered_vacancies


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
    data = custom_sort_vacancies(data, key_sort=sort_by_salaries)
    data = custom_filter_vacancies(data, FilterPresenceSalary(4))

    for el in data:
        print(el['alternate_url'])
        print(el['salary']['from'], el['salary']['to'])


if __name__ == '__main__':
    main()
