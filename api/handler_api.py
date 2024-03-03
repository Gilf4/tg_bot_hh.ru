import requests
from api.url_requests import *


async def send_requests(url: str, par: dict = None) -> any:
    """
    Функция для безопасного отправления запроса
    :param url: Ссылка на api
    :param par: Словарь опциональных параметров
    :return: Ответ в виде json'а или None, если произошла ошибка
    """

    req = requests.get(url, params=par)

    if req.status_code == 200:
        data = req.json()
        req.close()
        return data


async def get_areas_json() -> any:
    """
    Функция делает запрос для получения мест (https://api.hh.ru/areas)
    :return: словарь мест в виде json'а
    """

    return await send_requests(url_get_areas)


async def get_vacancies(params: dict) -> any:
    """
    Функция делает запрос для получения вакансий (https://api.hh.ru/vacancies)
    :param params: Словарь параметров для запроса
    :return: словарь в виде json'а
    """

    return await send_requests(url_get_vacancies, params)


async def main():
    data = await get_areas_json()
    print(data.get('Нижний Новгород'))


if __name__ == '__main__':
    main()
