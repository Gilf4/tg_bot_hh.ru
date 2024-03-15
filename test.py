import asyncio
from utils.utils import smarted_get_vacancies, custom_sort_vacancies
from utils.keys_sort import sort_by_salaries
from utils.managers import ClientManager
from utils.get_info import get_areas


async def main1():
    c = ClientManager()
    c.set_base_structure()
    c.change_query('Уборщик')

    data = await smarted_get_vacancies(c)
    # data = custom_filter_vacancies(data, FilterPresenceSalary(4))
    data = await custom_sort_vacancies(data, key_sort=sort_by_salaries)

    for el in data:
        print(el['alternate_url'])

        if el['salary']:
            print(el['salary']['from'], el['salary']['to'])
        else:
            print('Не указана')


if __name__ == '__main__':
    asyncio.run(main1())
