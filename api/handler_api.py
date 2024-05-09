import asyncio
from api.url_requests import *
from aiohttp.client import ClientSession


async def async_base_send_requests(url: str, session: ClientSession, params: dict | None = None) -> any:
    while True:
        async with session.get(url, params=params) as response:
            data = await response.json()
            # print(data)

            if not data.get('errors'):
                print(url)
                return data

        await asyncio.sleep(0.1)


async def async_get_vacancies(session: ClientSession, params: dict | None, out: list) -> any:
    async with session.get(url_get_vacancies, params=params) as response:
        data = await response.json()
        vacancies = data.get('items')
        # time.sleep(0.05)
        if vacancies:
            out.extend(vacancies)
        else:
            if response.status == 400:
                await asyncio.create_task(async_get_vacancies(session, params, out))


async def async_get_areas_json(session: ClientSession, params: dict) -> any:
    """
    Функция делает запрос для получения мест (https://api.hh.ru/areas)
    :return: словарь мест в виде json'а
    """

    return await async_base_send_requests(url_get_areas, session, params)


async def main():
    pass


if __name__ == '__main__':
    main()
