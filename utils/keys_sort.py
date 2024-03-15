from utils.params import P


def sort_by_salaries(vacancy: any) -> float:
    """
    Функция возращает параметр сортировки вакатсии. Если есть отрезок зарплат (от до), то возвращает
    верхнюю граници. Если зарплата не указана, то считаеться, что она равна
    невозможному минимуму: -1
    :param vacancy: Вакансия
    :return: Параметр сортировки
    """

    salary = vacancy.get(P.salary)
    if salary:
        return salary.get('to') or salary.get('from') or -1

    return -1
