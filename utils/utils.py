from collections import defaultdict
from api.handler_api import get_areas_json, get_vacancies, send_requests, get_list_of_salaries
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


def get_count_vacancies(query: str, area: str) -> int:
    """
    :param query: Запрос по вакансий (python developer, уборщик пятёрочки)
    :param area: Место поиска вакансий
    :return: Количество найденных вакансий
    """

    data = smarted_get_vacancies(query, area=area)  # Неоптимальная реализация. Проблемы со скоростью -> оптимизация
    return len(data)  # found - key


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


def format_skills(skills: dict, count_vacancies: int) -> str:
    """
    :param skills: Словарь вида {name_skill: count}, где count - количество вакансий с таким скиллом
    :param count_vacancies: Общее число вакансий
    :return: Сообщение о стеке технологий
    """

    message_lines = ['Стек по вашему запросу:']
    ind = 0

    # Сортировка ключей по частоте встречаемости
    name_skills = sorted(skills.keys(), key=lambda x: skills[x], reverse=True)

    for skill in name_skills:
        count_skill = skills[skill]
        percent_of = round(count_skill / count_vacancies * 100, 2)
        message_lines.append(f'{ind}) {skill} - {percent_of} % ({count_skill})')
        ind += 1

    if len(message_lines) == 1:
        message_lines[0] = 'Информация не найдена'

    return '\n'.join(message_lines)


def format_salary(salary_dict):
    if salary_dict:
        salary_from = salary_dict.get('from', 'Не указана')
        salary_to = salary_dict.get('to', 'Не указана')
        salary_currency = salary_dict.get('currency', '')
        # Преобразование None в "Не указана"
        if salary_from is None:
            salary_from = "Не указана"
        if salary_to is None:
            salary_to = "Не указана"
        if salary_to == "Не указана":
            return f"{salary_from} {salary_currency}"
        else:
            return f"{salary_from} - {salary_to} {salary_currency}"
    else:
        return "Зарплата не указана"


def format_vacancies(text):
    vacancies = get_vacancies(text)
    if vacancies:
        vacancies_text = ''
        for item in vacancies.get('items', []):
            salary_text = format_salary(item.get('salary'))
            vacancies_text += f"Название вакансии: {item['name']}\n"
            vacancies_text += f"Зарплата: {salary_text}\n"
            vacancies_text += f"Компания: {item['employer']['name']}\n"
            vacancies_text += f"Город: {item['area']['name']}\n"
            vacancies_text += f"URL вакансии: {item['alternate_url']}\n\n"
        if vacancies_text:
            return vacancies_text
        else:
            return "По вашему запросу ничего не найдено."
    else:
        return "Ошибка при запросе"


def calculate_average_salary(list_of_salaries):
    return statistics.median(list_of_salaries)


def sort_by_price_vacancies(list_vacancies: list, reverse=True) -> list:
    """
    Функция сортирукт вакансии по цене (костыль 1 - ой). Если есть отрезок зарплат (от до), то сортирует
    по верхней границе. Если зарплата не указана, то считаеться, что она равна
    невозможному минимуму: -1. Вакансии с зарплатами в других волютах убираються
    (костыль 2 - ой).
    :param list_vacancies: Список вакансий для сортировка
    :param reverse: Если True - сортирует по не возрастанию (включено по дефолту). Если False - по не убыванию
    :return: Новый отсортированный список
    """

    list_vacancies_ru = []

    for i in range(len(list_vacancies)):  # Костыль для других волют
        if list_vacancies[i]['salary']['currency'] == 'RUR':
            list_vacancies_ru.append(list_vacancies[i])

    list_vacancies_ru.sort(key=lambda x: x['salary']['to'] or x['salary']['from'] or -1, reverse=reverse)

    return list_vacancies_ru


def main():
    """
    Функция для быстрого теста или проверок
    """

    data = smarted_get_vacancies('Python')[:100]
    # extended_data = extend_vacancies(data)
    # skills = get_skills(extended_data)
    # message = format_skills(skills, len(extended_data))
    # print(message)
    data = sort_by_price_vacancies(data)

    for el in data:
        print(el['alternate_url'])
        print(el['salary']['from'], el['salary']['to'])


if __name__ == '__main__':
    main()
