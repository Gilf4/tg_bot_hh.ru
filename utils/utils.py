from collections import defaultdict
import copy
import asyncio
import aiohttp
from api.handler_api import async_get_vacancies, async_base_send_requests
from utils.formats import format_vacancies, format_skills
from utils.keys_sort import sort_by_salaries
from utils.filters import FilterPresenceSalary
from utils.managers import ClientManager
from utils.params import P


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

    if c.get_is_new_vacancies() and not count_vacancies:
        return c.get_vacancies()
    elif c.get_is_new_vacancies() and count_vacancies:
        return c.get_vacancies()[:count_vacancies]

    data = await async_get_all_vacancies2(c)

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


async def get_extend_vacancies(c: ClientManager, count: int = 200) -> tuple | list:
    """
        Функция для получения расширенных данный о вакансии. Работает медленно!
        :param c: экземпляр ClientManager
        :param count: количество вакансий
        :return: список с расширенныйми вакансиями
        """

    vacancies = await smarted_get_vacancies(c, count)
    return await extend_vacancies(vacancies)


async def extend_vacancies(list_vacancies: list) -> tuple | list:
    """
    Функция расширяет информацию о вакансиях.
    :param list_vacancies: список вакансий для расширения. Предпочтительнее, взятых из smarted_get_vacancies
    :return: список расширенных вакансий
    """

    connector = aiohttp.TCPConnector(limit=150)

    async with aiohttp.ClientSession(headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }, connector=connector) as session:
        tasks = []

        for vacancy in list_vacancies:
            url = vacancy.get(P.url)  # Получение ссылки на данные со страницы вакансии

            if url:
                task = asyncio.create_task(async_base_send_requests(url, session))
                tasks.append(task)
            else:
                continue

        data = await asyncio.gather(*tasks)

    return data


async def get_skills(extended_vacancies: list) -> dict:
    """
    :param extended_vacancies: Список расширенных вакансий
    :return: Словарь вида {name_skill: count}, где count - количество вакансий с таким скиллом
    """

    skills = defaultdict(int)

    for vacancy in extended_vacancies:
        if vacancy:
            for skill in vacancy.get(P.key_skills, []):
                skills[skill[P.name]] += 1
        else:
            # print('Нет вакансий')
            pass

    return skills


async def get_format_skills(c: ClientManager) -> str:
    """
    Функция для получения форматированного сообщения о стеке технологий по запросу
    :param c: Параметры для получения вакансии в виде ClientManager
    :return: Форматированное сообщение о стеке технологий
    """

    extended_data = await get_extend_vacancies(c)
    skills = await get_skills(extended_data)
    message = format_skills(skills, len(extended_data))

    return message


async def get_format_vacancies(c: ClientManager):
    """
    :param c: Параметры для получения вакансии в виде ClientManager.r
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
    Функция сортирует вакансии по параметру, который задаётся ключём сортировки. Сортирует на месте.
    :param vacancies: Список вакансий для сортировка
    :param key_sort: Функция, указывающая, параметр по которому будет производиться сортировка
    :param reverse: Если True - сортирует по не возрастанию (включено по дефолту). Если False - по не убыванию
    :return: Отсортированный список
    """

    vacancies.sort(key=key_sort, reverse=reverse)
    return vacancies


async def custom_filter_vacancies(vacancies: list, *args) -> list:
    """
    Функция для фильтрации вакансий
    :param vacancies: вакансии для вильтрации
    :param args: совокупность фильтров для вакансий, переданных через запятую
    :return: Новый отфильтрованый список
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
        salary = get_salary(vacancy)
        if salary and salary[0] == 1:
            salaries.append(sum(salary) / 2)
        elif salary:
            salaries.append(salary[1])

    return salaries


def get_salary(vacancy: dict):
    salary = vacancy.get('salary')
    if not salary:
        return

    from_value = salary.get('from')
    to_value = salary.get('to')

    if from_value and to_value:
        return 1, from_value, to_value
    elif from_value:
        return 2, from_value
    elif to_value:
        return 3, to_value


async def main():
    c = ClientManager(query='Уборщик')

    data = await smarted_get_vacancies(c.get_request_parameters())
    data = await custom_sort_vacancies(data, key_sort=sort_by_salaries)
    data = await custom_filter_vacancies(data, FilterPresenceSalary(4))

    for el in data:
        print(el['alternate_url'])
        print(el['salary']['from'], el['salary']['to'])


if __name__ == '__main__':
    main()
