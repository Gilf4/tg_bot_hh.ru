import asyncio
from utils.filters import FilterSkills
from utils import utils
from utils.params import P
from utils.managers import ClientManager
from utils.get_info import get_areas


async def get_vacancies(query: str, area: str, skills: list[str]) -> list:
    c = ClientManager(query=query, area=area)
    count = 2000

    # Скилы есть только в расширенный вакансиях
    extend_vacancies = await utils.get_extend_vacancies(c, count=count)
    extend_vacancies = await utils.custom_filter_vacancies(extend_vacancies, FilterSkills(
        skills))

    return extend_vacancies


async def main():
    skills = [['Python', 'SQL', 'PostgreSQL', 'Git', 'Linux'],
              []]

    vacancies = get_vacancies('Python', 'Нижний Новгород', skills[0])


if __name__ == '__main__':
    asyncio.run(main())
