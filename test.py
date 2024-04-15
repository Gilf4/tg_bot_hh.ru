import asyncio
import utils.utils as u
import utils.filters as fil
from utils.params import P
from utils.managers import ClientManager
from utils.get_info import get_areas
from utils.formats import format_skills


async def main():
    c = ClientManager()
    c.set_base_structure()
    c.change_query('Python')

    count = 200
    data = await u.smarted_get_vacancies(c, count_vacancies=count)
    extended_data = await u.extend_vacancies(data)
    print(len(data), len([i for i in extended_data if i]))

    s = await u.custom_filter_vacancies(c.get_vacancies(), fil.FilterSkills(['Python', 'SQL', 'PostgreSQL', 'Git', 'Linux']))
    skills = await u.get_skills(s)
    message = format_skills(skills, len(extended_data))
    print(s[0].get(P.key_skills))
    print(message)


if __name__ == '__main__':
    asyncio.run(main())
