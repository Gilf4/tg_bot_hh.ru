from collections import defaultdict
import copy
import asyncio
import aiohttp
from api.url_requests import url_get_vacancies
from api.handler_api import async_send_requests, async_get_vacancies, async_send_requests_skil
from utils.formats import format_vacancies, format_skills
from utils.keys_sort import sort_by_salaries
from utils.filters import FilterPresenceSalary
from utils.managers import ClientManager
from utils.params import P


# async def get_all_vacancies(c: ClientManager):
#     page = -1  # Сдвиг для красоты (первая страница - 0)
#     data = []  # Список вакансий
#     c.change_search_per_page(100)  # Устоновка максимального количество получаемых вакансий
#
#     while True:
#         page += 1
#         c.change_search_page(page)
#         vacancies = await async_get_vacancies(c.get_request_parameters())
#
#         if vacancies and vacancies['items']:
#             data.extend(vacancies['items'])
#         else:
#             break
#
#         if page == vacancies.get('pages'):  # Проверка на последнюю стнаницу
#             break
#
#     return data

#
# async def async_get_all_vacancies(c: ClientManager):
#     c.change_search_per_page(100)  # Устоновка максимального количество получаемых вакансий
#     vacancies = []
#
#     async with aiohttp.ClientSession() as session:
#         response = await session.get(url_get_vacancies, params=c.get_request_parameters())
#         response = await response.json()
#         pages = response.get('pages')
#
#         tasks = []
#
#         for page in range(pages):
#             c.change_search_page(page)
#             task = asyncio.create_task(async_get_vacancies(session, copy.deepcopy(c.get_request_parameters()), vacancies))
#             tasks.append(task)
#
#         await asyncio.gather(*tasks)
#
#     return vacancies


async def async_get_all_vacancies2(c: ClientManager):
    c.change_search_per_page(100)  # Устоновка максимального количество получаемых вакансий
    vacancies = []

    async with aiohttp.ClientSession(headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }) as session:
        tasks = []

        for page in range(20):
            c.change_search_page(page)
            task = asyncio.create_task(async_get_vacancies(session, copy.deepcopy(c.get_request_parameters()), vacancies))
            tasks.append(task)

        await asyncio.gather(*tasks)

    return vacancies


async def smarted_get_vacancies(c: ClientManager, count_vacancies: int = 0) -> list:
    """
    Функция возвращает n - ое количество вакансий или максимум вакансий, который есть (может быть [ ]).
    :param count_vacancies: Количестов запрашиваемых вакансий. Если нужны все, то можно ничего не указывать или указать 0
    :param c: Параметры для получения вакансии в виде словаря. Для приготовленя рекомундуеться params_get_vacancies
    :return: Список вакансий
    """
    print(c.get_is_new_vacancies())
    if c.get_is_new_vacancies() and not count_vacancies:
        return c.get_vacancies()
    elif c.get_is_new_vacancies() and count_vacancies:
        return c.get_vacancies()[:count_vacancies]

    from time import time

    start = time()
    data = await async_get_all_vacancies2(c)
    print(f'{time() - start}')

    filters = c.get_filters()

    if filters:
        data = await custom_filter_vacancies(data, *filters)

    c.change_vacancies(data)
    c.change_is_new_vacancies(True)
    await c.save()

    if count_vacancies:
        data = data[:count_vacancies]  # Срезаем лишнии вакансии

    return data


async def get_count_vacancies(c: ClientManager) -> int:
    """
    :param c: Параметры для получения вакансии в виде словаря. Для приготовленя рекомундуеться params_get_vacancies
    :return: Количество найденных вакансий
    """

    data = await smarted_get_vacancies(c)
    return len(data)


async def extend_vacancies(list_vacancies: list) -> list:
    """
    Функция расширяет информацию о вакансиях. Работает очень медлено, 1 - 4 с. одна вакансия!
    :param list_vacancies: список вакансий для расширения. Предпочтительнее, взятых из smarted_get_vacancies
    :return: список расширенных вакансий
    """

    data = []

    async with aiohttp.ClientSession(headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }) as session:
        tasks = []

        for vacancy in list_vacancies:
            url = vacancy.get(P.url)  # Получение ссылки на данные со страницы вакансии

            if url:
                task = asyncio.create_task(async_send_requests_skil(url, session, None, data))
                tasks.append(task)
            else:
                continue

        await asyncio.gather(*tasks)

    return data


async def get_skills(extended_vacancies: list) -> dict:
    """
    :param extended_vacancies: Список расширенных вакансий
    :return: Словарь вида {name_skill: count}, где count - количество вакансий с таким скиллом
    """

    skills = defaultdict(int)

    for vacancy in extended_vacancies:
        for skill in vacancy.get(P.key_skills, []):
            skills[skill[P.name]] += 1

    return skills


async def get_format_skills(c: ClientManager) -> str:
    """
    Функция для получения форматированного сообщения о стеке технологий по запросу. Работает медлено!
    :param c: Параметры для получения вакансии в виде ClientManager
    :return: Форматированное сообщение о стеке технологий
    """

    count = 300
    data = await smarted_get_vacancies(c, count_vacancies=count)
    extended_data = await extend_vacancies(data)
    print(len(data))
    skills = await get_skills(extended_data)
    print(len(skills))

    message = format_skills(skills, len(extended_data))

    return message


async def get_format_vacancies(c: ClientManager):
    """
    :param c: Параметры для получения вакансии в виде ClientManager
    :return:
    """

    f = True
    vacancies = await smarted_get_vacancies(c)
    if len(vacancies) <= (c.get_page() + 1) * c.get_per_page():
        f = False

    vacancies = vacancies[c.get_page() * c.get_per_page(): (c.get_page() + 1) * c.get_per_page()]

    return format_vacancies(vacancies), f


async def calculate_median(data: list) -> float | bool:
    """
    Return the median (middle value) of numeric data.

        When the number of data points is odd, return the middle data point.
        When the number of data points is even, the median is interpolated by
        taking the average of the two middle values:
    """

    data = sorted(data)
    n = len(data)
    if n == 0:
        return False
    if n % 2 == 1:
        return data[n // 2]
    else:
        i = n // 2
        return (data[i - 1] + data[i]) / 2


async def calculate_average(data: list) -> float | bool:
    """
    Функция для счёта среднего значения по списку элементов
    :param data: Список элементов
    :return: Среднее значение
    """

    if data:
        return round(sum(data) / len(data), 2)

    return False


async def custom_sort_vacancies(vacancies: list, key_sort: any, reverse=True) -> list:
    """
    Функция сортирукт вакансии по параметру, который задаётся ключём сортировки (костыль 1 - ый,
    - сортировка уже полученных данных, а не сортировка при запросе данных).
    (костыль 2 - ой, - отсутствие конвертации валюты)
    :param vacancies: Список вакансий для сортировка
    :param key_sort: Функция, указывающая, параметр по которому будет производиться сортировка
    :param reverse: Если True - сортирует по не возрастанию (включено по дефолту). Если False - по не убыванию
    :return: Новый отсортированный список
    """

    vacancies.sort(key=key_sort, reverse=reverse)
    return vacancies


async def custom_filter_vacancies(vacancies: list, *args) -> list:
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


async def get_salaries(c: ClientManager) -> list:
    salaries = []
    vacancies = await smarted_get_vacancies(c)

    if not vacancies:
        return []

    for vacancy in vacancies:
        salary = vacancy.get('salary')

        if salary:
            from_value = salary.get('from')
            to_value = salary.get('to')
            if from_value and to_value:
                salaries.append((from_value + to_value) / 2)
            elif from_value:
                salaries.append(from_value)
            elif to_value:
                salaries.append(to_value)

    return salaries


async def main():
    c = ClientManager()
    c.set_base_structure()
    c.change_query('Уборщик')

    data = await smarted_get_vacancies(c.get_request_parameters())
    data = await custom_sort_vacancies(data, key_sort=sort_by_salaries)
    data = await custom_filter_vacancies(data, FilterPresenceSalary(4))

    for el in data:
        print(el['alternate_url'])
        print(el['salary']['from'], el['salary']['to'])


if __name__ == '__main__':
    main()
