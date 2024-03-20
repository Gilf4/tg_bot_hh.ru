from aiogram.fsm.context import FSMContext
from utils.params import P
from utils.get_info import get_areas
from utils.filters import FilterSalaryFrom, FilterSalaryTo


class ClientManager:
    def __init__(self):
        self.data: dict = {}
        self.profile = None
        self.state: FSMContext | None = None

    async def init(self, state: FSMContext):
        self.state = state

        if type(state) is not FSMContext:
            print('Не потдерживаемый тип данных - ', type(state))
            return

        data = await state.get_data()

        if not data:
            print('Необходимая структура не найдена - ', 'await state.get_data() = ', data)
            return

        self.data = data

        ind_profile = self.data.get(P.ind_profile)
        if not ind_profile:
            print('Необходимая структура не найдена - ', data)
            return

        profiles = self.data.get(P.profiles)
        if not profiles:
            print('Необходимая структура не найдена - ', data)
            return

        profile = profiles.get(ind_profile)
        if type(profile) is not dict:
            print('Необходимая структура не найдена - ', data)
            return
        
        self.profile = profile

        return True

    def set_base_structure(self, name_profile: str = None):
        """
        Возвращаект базовую структуру не временных данных пользователя. В виде:
        {P.ind_profile: P.base, P.profiles: {P.base: {P.request_parameters: {}, P.filters: [], P.sorts: []}}}
        """

        if name_profile is None:
            self.data[P.ind_profile] = P.base
        else:
            self.data[P.ind_profile] = name_profile

        self.data[P.profiles] = dict()
        self.data[P.profiles][P.base] = dict()
        self.data[P.profiles][P.base][P.filters] = []
        self.data[P.profiles][P.base][P.sorts] = []
        self.data[P.profiles][P.base][P.vacancies] = []
        self.data[P.profiles][P.base][P.request_parameters] = dict()
        self.data[P.profiles][P.base][P.page] = 0
        self.data[P.profiles][P.base][P.per_page] = 5
        self.data[P.profiles][P.base][P.is_new_vacancies] = False
        self.data[P.profiles][P.base][P.revers_sort] = True

    async def set_state(self, condition):
        await self.state.set_state(condition)

    def change_query(self, query):
        self.profile[P.request_parameters][P.text] = query
        return True

    def change_area(self, area: str):
        areas = get_areas()

        if areas.get(area.lower()):
            self.profile[P.request_parameters][P.area] = areas[area.lower()]
            return True

        print('Город - ', area, ' не найден')
        return False

    def change_search_field(self, search_field):
        self.profile[P.request_parameters][P.search_field] = search_field
        return True

    def change_salary(self, salary: str):
        if ('-' in salary) and (len(salary.split('-')) == 2):
            salary = salary.strip()
            for i in salary:
                if not i.isdigit() and (i != '-'):
                    return False

            salary_from, salary_to = map(int, salary.split('-'))
            self.profile[P.filters].append(FilterSalaryFrom(salary_from))
            self.profile[P.filters].append(FilterSalaryTo(salary_to))

            return True
        return False

    def change_revers_sort(self, is_revers_sort):
        self.profile[P.revers_sort] = is_revers_sort
        return True

    def change_key_sort(self, key_sort):
        self.profile[P.key_sort] = key_sort
        return True

    def change_is_new_vacancies(self, is_new_vacancies):
        self.data[P.profiles][P.base][P.is_new_vacancies] = is_new_vacancies
        return True

    def change_per_page(self, per_page):
        self.data[P.profiles][P.base][P.per_page] = per_page
        return True

    def change_search_per_page(self, per_page):
        self.data[P.profiles][P.base][P.request_parameters][P.per_page] = per_page
        return True

    def change_experience(self, experience):
        if experience:
            self.profile[P.request_parameters][P.experience] = experience
        else:
            if self.profile[P.request_parameters].get(P.experience):
                del self.profile[P.request_parameters][P.experience]

        return True

    def change_page(self, page):
        self.data[P.profiles][P.base][P.page] = page
        return True

    def change_search_page(self, page):
        self.data[P.profiles][P.base][P.request_parameters][P.page] = page
        return True

    def change_vacancies(self, vacancies):
        self.data[P.profiles][P.base][P.vacancies] = vacancies
        return True

    def get_request_parameters(self):
        return self.profile.get(P.request_parameters)

    def get_query(self):
        query = self.profile.get(P.request_parameters, {}).get(P.text)
        return query

    def get_area(self):
        area = self.profile.get(P.request_parameters, {}).get(P.area)
        return area

    def get_salary(self):
        salary = self.profile.get(P.request_parameters, {}).get(P.salary)
        return salary

    def get_per_page(self):
        per_page = self.profile.get(P.per_page)
        return per_page

    def get_search_per_page(self):
        search_per_page = self.profile.get(P.request_parameters, {}).get(P.search_per_page)
        return search_per_page

    def get_page(self):
        page = self.profile.get(P.page)
        return page

    def get_search_page(self):
        search_page = self.profile.get(P.request_parameters, {}).get(P.search_page)
        return search_page

    def get_filters(self):
        return self.profile.get(P.filters)

    def get_is_new_vacancies(self):
        return self.profile.get(P.is_new_vacancies)

    def get_experience(self):
        return self.profile.get(P.request_parameters, {}).get(P.experience)

    def get_vacancies(self):
        return self.profile.get(P.vacancies)

    def get_revers_sort(self):
        return self.profile.get(P.revers_sort)

    def get_key_sort(self):
        return self.profile.get(P.key_sort)

    def get_search_field(self):
        return self.profile.get(P.request_parameters, {}).get(P.search_field)

    async def save(self):
        await self.state.update_data(self.data)
