
def format_vacancies(vacancies):
    if not vacancies:
        return 'Нет подходящих вакансий'

    vacancies_text = ''
    for item in vacancies:
        salary_text = format_salary(item.get('salary'))
        vacancies_text += f"Название вакансии: {item['name']}\n"
        vacancies_text += f"Зарплата: {salary_text}\n"
        vacancies_text += f"Компания: {item['employer']['name']}\n"
        vacancies_text += f"Город: {item['area']['name']}\n"
        vacancies_text += f"URL вакансии: {item['alternate_url']}\n\n"
    if vacancies_text:
        return vacancies_text
    else:
        return "По вашему запросу ничего не найдено."


def format_salary(salary_dict):
    if salary_dict:
        salary_from = salary_dict.get('from', 'Не указана')
        salary_to = salary_dict.get('to', 'Не указана')
        salary_currency = salary_dict.get('currency', '')
        # Преобразование None в "Не указана"
        if salary_from is None:
            salary_from = "Не указана"
        if salary_to is None:
            salary_to = "Не указана"
        if salary_to == "Не указана":
            return f"{salary_from} {salary_currency}"
        else:
            return f"{salary_from} - {salary_to} {salary_currency}"
    else:
        return "Зарплата не указана"


def format_skills(skills: dict, count_vacancies: int) -> str:
    """
    :param skills: Словарь вида {name_skill: count}, где count - количество вакансий с таким скиллом
    :param count_vacancies: Общее число вакансий
    :return: Сообщение о стеке технологий
    """

    message_lines = ['Стек по вашему запросу:']
    ind = 0

    # Сортировка ключей по частоте встречаемости
    name_skills = sorted(skills.keys(), key=lambda x: skills[x], reverse=True)[:51]

    for skill in name_skills:
        count_skill = skills[skill]
        percent_of = round(count_skill / count_vacancies * 100, 2)
        message_lines.append(f'{ind}) {skill} - {percent_of} % ({count_skill})')
        ind += 1

    if len(message_lines) == 1:
        message_lines[0] = 'Информация не найдена'

    return '\n'.join(message_lines)
