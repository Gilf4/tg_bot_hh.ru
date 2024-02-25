from utils.utils import smarted_get_vacancies, custom_sort_vacancies, custom_filter_vacancies
from utils.keys_sort import sort_by_salaries
from utils.filters import FilterPresenceSalary


def main1():
    data = smarted_get_vacancies('ML')
    # data = custom_filter_vacancies(data, FilterPresenceSalary(4))
    data = custom_sort_vacancies(data, key_sort=sort_by_salaries)

    for el in data:
        print(el['alternate_url'])

        if el['salary']:
            print(el['salary']['from'], el['salary']['to'])
        else:
            print('Не указана')


if __name__ == '__main__':
    main1()
