import time
import asyncio
from api.url_requests import *
from aiohttp.client import ClientSession


# headers={
#                 'User-Agent': 'MyApp/1.0 (my-app-feedback@example.com)',
#                 'HH-User-Agent': 'MyApp/1.0 (my-app-feedback@example.com)',
#                 'Content-Type': 'application/x-www-form-urlencoded'}

async def async_send_requests(url: str, session: ClientSession, params: dict, out: list) -> any:
    async with session.get(url, params=params, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }) as response:

        data = await response.json()
        vacancies = data.get('items')
        # time.sleep(0.05)
        if vacancies:
            # print(response.url)
            out.extend(vacancies)
        else:
            await asyncio.create_task(async_send_requests(url, session, params, out))
            # if response.status != 400:
            print(response.status)
            print(await response.json())


async def async_get_areas_json(session: ClientSession, params: dict, out: list) -> any:
    """
    Функция делает запрос для получения мест (https://api.hh.ru/areas)
    :return: словарь мест в виде json'а
    """

    return await async_send_requests(url_get_areas, session, params, out)


async def async_get_vacancies(session: ClientSession, params: dict, out: list) -> any:
    await async_send_requests(url_get_vacancies, session, params, out)


async def main():
    pass


if __name__ == '__main__':
    main()
