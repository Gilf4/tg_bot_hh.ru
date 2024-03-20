from dataclasses import dataclass


@dataclass
class ParamsOnlyWithSalary:
    true: bool = True
    false: bool = False


@dataclass
class ParamsValuesSearchField:
    name: str = 'name'


@dataclass
class ParamsValuesOrderBy:
    publication_time: str = 'publication_time'


@dataclass
class P:
    text: str = 'text'
    per_page: int = 'per_page'
    page: int = 'page'
    area: str = 'area'
    only_with_salary: bool = 'only_with_salary'
    search_field: str = 'search_field'
    order_by: str = 'order_by'

    values_only_with_salary: ParamsOnlyWithSalary = ParamsOnlyWithSalary
    values_search_field: ParamsValuesSearchField = ParamsValuesSearchField
    values_order_by: ParamsValuesOrderBy = ParamsValuesOrderBy

    true: bool = True  # Для полноты относительно values-параметров
    false: bool = False
    name: str = 'name'
    publication_time: str = 'publication_time'

    profiles: str = 'profiles'
    ind_profile: str = 'ind_profile'
    request_parameters: str = 'request_parameters'
    salary: str = 'salary'
    filters: str = 'filters'
    sorts: str = 'sorts'

    base: str = 'base'
    id_profile: str = 'id_profile'

    found: str = 'found'
    url: str = 'url'
    key_skills: str = 'key_skills'

    vacancies: str = 'vacancies'
    is_new_vacancies: str = 'is_new_vacancies'
    search_page: str = 'search_page'
    search_per_page: str = 'search_per_page'
    experience: str = 'experience'
    revers_sort: str = 'revers_sort'
    key_sort: str = 'key_sort'


def main():
    """
    Пример создания / заполнения словаря значений для get_vacancies
    """

    params = dict()
    params[P.text] = 'Python'
    params[P.area] = 'Нижний Новгород'
    params[P.per_page] = 100
    params[P.page] = 10
    params[P.only_with_salary] = P.values_only_with_salary.true
    params[P.order_by] = P.values_order_by.publication_time
    params[P.search_field] = P.values_search_field.name

    return params


if __name__ == '__main__':
    main()
