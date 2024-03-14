from aiogram.fsm.context import FSMContext
from utils.params import P


class ClientManager:
    def __init__(self):
        self.data = None
        self.profile = None

    async def init(self, state: FSMContext):
        if type(state) is not FSMContext:
            print('Не потдерживаемый тип данных')
            return

        data = await state.get_data()

        if not data:
            print('Необходимая структура не найдена')
            return

        self.data = data

        ind_profile = self.data.get(P.ind_profile)
        if not ind_profile:
            print('Необходимая структура не найдена')
            return

        profiles = self.data.get(P.profiles)
        if not profiles:
            print('Необходимая структура не найдена')
            return

        profile = profiles.get(ind_profile)
        if type(profile) is not dict:
            print('Необходимая структура не найдена')
            return
        
        self.profile = profile
        
    def save_query(self, query):
        self.profile[P.request_parameters][P.text] = query
        return True

    def get_query(self):
        query = self.profile.get(P.request_parameters, {}).get(P.text)
        return query

    def save_area(self, areas):
        self.profile[P.request_parameters][P.area] = areas
        return True

    def get_area(self):
        area = self.profile.get(P.request_parameters, {}).get(P.area)
        return area

    def save_salary(self, salary):
        self.profile[P.salary] = int(salary)

    def get_salary(self):
        salary = self.profile.get(P.request_parameters, {}).get(P.salary)
        return salary
    