from dataclasses import dataclass


@dataclass
class ParamsOnlyWithSalary:
    key_true: bool = True
    key_false: bool = False


@dataclass
class ParamsValuesSearchField:
    key_name: str = 'name'


@dataclass
class ParamsValuesOrderBy:
    key_publication_time: str = 'publication_time'


@dataclass
class Params:
    key_text: str = 'text'
    key_per_page: int = 'per_page'
    key_page: int = 'page'
    key_area: str = 'area'
    key_only_with_salary: bool = 'only_with_salary'
    key_search_field: str = 'search_field'
    key_order_by: str = 'order_by'

    values_only_with_salary: ParamsOnlyWithSalary = ParamsOnlyWithSalary
    values_search_field: ParamsValuesSearchField = ParamsValuesSearchField
    values_order_by: ParamsValuesOrderBy = ParamsValuesOrderBy


def main():
    """
    Пример создания / заполнения словаря значений для get_vacancies
    """

    params = dict()
    params[Params.key_text] = 'Python'
    params[Params.key_area] = 'Нижний Новгород'
    params[Params.key_per_page] = 100
    params[Params.key_page] = 10
    params[Params.key_only_with_salary] = Params.values_only_with_salary.key_true
    params[Params.key_order_by] = Params.values_order_by.key_publication_time
    params[Params.key_search_field] = Params.values_search_field.key_name

    return params


if __name__ == '__main__':
    main()
