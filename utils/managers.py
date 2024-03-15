from aiogram.fsm.context import FSMContext
from utils.params import P
from utils.get_info import get_areas


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

    def set_base_structure(self):
        """
        Возвращаект базовую структуру не временных данных пользователя. В виде:
        {P.ind_profile: P.base, P.profiles: {P.base: {P.request_parameters: {}, P.filters: [], P.sorts: []}}}
        """
        
        self.data[P.ind_profile] = P.base
        self.data[P.profiles] = dict()
        self.data[P.profiles][P.base] = dict()
        self.data[P.profiles][P.base][P.request_parameters] = dict()
        self.data[P.profiles][P.base][P.filters] = []
        self.data[P.profiles][P.base][P.sorts] = []

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

    def change_salary(self, salary):
        self.profile[P.salary] = int(salary)
        return True

    def change_per_page(self, per_page):
        self.profile[P.request_parameters][P.per_page] = per_page
        return True

    def change_page(self, page):
        self.profile[P.request_parameters][P.page] = page
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
        per_page = self.profile.get(P.request_parameters, {}).get(P.per_page)
        return per_page

    def get_page(self):
        page = self.profile.get(P.request_parameters, {}).get(P.page)
        return page

    async def save(self):
        await self.state.update_data(self.data)
