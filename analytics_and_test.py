import asyncio
import matplotlib.pyplot as plt
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
    skills = [['Python', 'Метматика', 'Английский язык', 'Алгоритмы', 'Математический анализ',
               'Аналитическая Геометрия', 'Линейная алгебра', 'Дискретная математика', 'искусственный интеллект'],
              ['Архитектура ЭВМ', 'ЭВМ', 'Базы данных', 'SQL', 'Сети и телекоммуникации', 'Теория вероятностей',
               'Матемматическая Статистика',
               'Языки программирования для анализа данных', 'R', 'DevOps', 'Технология разработки программных систем', 'Филосовия'],
              ['Методы машинного обучения и искусственного интеллекта', 'Machine learning', 'deep learning',
               'Java', 'Глубокое обучение', 'Обучение с подкреплением', 'Технологии "мягких вычислений',
               'Предиктивные модели и прикладная аналитика', 'HTML', 'css'],
              ['Кибернетика', 'Прикладные задачи искусственного интеллекта', 'Технологии MLOps',
               'Теория систем и системный анализ', 'Математическая логика и исследование операций',
               'Математическая логика и исследование операций', 'Компьютерное зрение', 'Обработка естественного языка',
               'NLP', 'Распознавание и синтез речи']]

    local_skills = []
    vacancies_for_ = []
    for els in skills:
        local_skills.extend(els)
        vacancies = await get_vacancies('Python', None, local_skills)
        vacancies_for_.append(vacancies)
        print(len(vacancies))

    x = [1, 2, 3, 4]
    y = list(map(len, vacancies_for_))

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()


if __name__ == '__main__':
    asyncio.run(main())
