import asyncio
from utils.filters import FilterSkills
from utils import utils
from utils.params import P
from utils.managers import ClientManager
from utils.get_info import get_areas
from utils.formats import format_skills


async def main():
    c = ClientManager(query='Python', area='Нижний Новгород')
    count = 2000

    skils = [[],
             [],
             [],
             []]

    # Скилы есть только в расширенный вакансиях
    extend_vacancies = await utils.get_extend_vacancies(c, count=count)
    extend_vacancies = await utils.custom_filter_vacancies(extend_vacancies, FilterSkills(['Python', 'SQL', 'PostgreSQL', 'Git', 'Linux']))
    skills = await utils.get_skills(extend_vacancies)

    print(len(extend_vacancies))
    print(format_skills(skills, len(extend_vacancies)))


if __name__ == '__main__':
    asyncio.run(main())
