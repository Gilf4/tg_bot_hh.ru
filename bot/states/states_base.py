from aiogram.fsm.state import StatesGroup, State


class StepsBase(StatesGroup):
    GET_QUERY = State()
    BASE_WORK = State()
