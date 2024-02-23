from api.handler_api import get_areas_json, get_vacancies, get_list_of_salaries
import statistics


def json_areas_to_dict(areas_tree: any, areas: dict) -> None:
    for area in areas_tree:
        areas[area['name']] = area['id']

        if area.get('areas'):
            json_areas_to_dict(area['areas'], areas)


def get_areas():
    """
    :return: return dict {name: number name}
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


def main():
    # 'from': 100000, 'to': None
    # data = json.dumps(data)
    data = smarted_get_vacancies('python')
    # print(data)
    print(len(data))


if __name__ == '__main__':
    main()
