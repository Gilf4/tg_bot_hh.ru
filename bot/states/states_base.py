from aiogram.fsm.state import StatesGroup, State


class StepsBase(StatesGroup):
    GET_QUERY = State()
    GET_FILTER = State()
    GET_SORTS = State()
    GET_AREA = State()
    GET_SEARCH_FIELD = State()
    BASE_WORK = State()
