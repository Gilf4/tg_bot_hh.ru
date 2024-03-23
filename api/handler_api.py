import time
import asyncio
from api.url_requests import *
from aiohttp.client import ClientSession


async def async_send_requests_skil(url: str, session: ClientSession, params: dict | None, out: list) -> any:
    async with session.get(url, params=params) as response:
        data = await response.json()

        # time.sleep(0.05)
        if not data.get('errors'):
            out.append(data)


async def async_send_requests(url: str, session: ClientSession, params: dict | None, out: list) -> any:
    async with session.get(url, params=params) as response:
        data = await response.json()
        vacancies = data.get('items')
        # time.sleep(0.05)
        if vacancies:
            out.extend(vacancies)
        else:
            if response.status == 400:
                print(response.status)
                print(await response.json())
                await asyncio.create_task(async_send_requests(url, session, params, out))
            elif response.status != 200:
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
