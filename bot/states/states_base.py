from aiogram.fsm.state import StatesGroup, State


class StepsBase(StatesGroup):
    GET_QUERY = State()
    GET_AREA = State()
    GET_SEARCH_FIELD = State()
    GET_SALARY = State()
    GET_NAME_PROFILE = State()
    BASE_WORK = State()
