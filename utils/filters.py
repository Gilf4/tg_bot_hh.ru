from utils.params import P


class FilterPresenceSalary:
    def __init__(self, mode: int = 3):
        """
        Клас для фильтрации вакансии по присутствию / отсутствию параметров цены.

        mode - 4: присутствие from и to параметров

        mode - 3: присутствие from или to параметра

        mode - 2: присутствие to параметра

        mode - 1: присутствие from параметра

        mode - 0: отсутствие from и to параметров
        :param mode: режим работы
        """

        self.mode = mode

    def is_(self, vacancy: any) -> bool:
        salary = vacancy.get('salary')

        if not salary:
            salary = {'from': False, 'to': False}

        if self.mode == 4:
            return salary['from'] and salary['to']
        elif self.mode == 3:
            return salary['from'] or salary['to']
        elif self.mode == 2:
            return salary['to']
        elif self.mode == 1:
            return salary['from']
        elif self.mode == 0:
            return not (salary['from'] or salary['to'])

        print('Ты что-то перепутал')
        print(0 / 0)


class FilterCurrency:
    def __init__(self, currency: str):
        self.currency = currency

    def is_(self, vacancy: any) -> bool:
        currency = vacancy.get('salary')

        if currency:
            return currency.get('currency') == self.currency

        return False


class FilterSalaryFrom:
    def __init__(self, salary_from: int):
        """
        :param salary_from: запрлата
        """

        self.salary_from = salary_from

    def is_(self, vacancy: any) -> bool:
        salary = vacancy.get('salary')

        if not salary:
            return False

        salary_from, salary_to = vacancy.get('from'), salary.get('to')

        if salary_to:
            if self.salary_from < salary_to:
                return True
        elif salary_from and not salary_to:
            return True

        return False


class FilterSalaryTo:
    def __init__(self, salary_to: int):
        """
        :param salary_to: запрлата
        """

        self.salary_to = salary_to

    def is_(self, vacancy: any) -> bool:
        salary = vacancy.get('salary')

        if not salary:
            return True

        salary_from, salary_to = vacancy.get('from'), salary.get('to')

        if salary_to:
            if self.salary_to < salary_to:
                return False
        elif salary_from and not salary_to:
            return False

        return True


class FilterSkills:
    def __init__(self, skills: list[str]):
        self.skills = list(map(lambda x: x.lower(), skills))

    def is_(self, vacancy: any) -> bool:
        if not vacancy:
            return True

        for skill in vacancy.get(P.key_skills, ()):
            print(vacancy.get(P.key_skills, ()))

            if skill.lower() not in self.skills:
                return False

        return True
