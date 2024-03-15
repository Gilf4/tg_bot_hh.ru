from api.handler_api import get_areas_json
from utils.params import P


def json_areas_to_dict(areas_json: any, areas: dict) -> None:
    """
    Функциа рекурсивного парсинка json'а мест
    :param areas_json: json мест
    :param areas: Словарь куда будут складываться найденные значения
    """

    for area in areas_json:
        areas[area[P.name]] = area['id']

        if area.get('areas'):
            json_areas_to_dict(area['areas'], areas)


async def get_areas():
    """
    :return: Cловарь мест в виде {area_lower: number} и {number: area}. Где number - индефикатор места
    """

    areas_tree = await get_areas_json()
    areas = dict()
    json_areas_to_dict(areas_tree, areas)

    for name in list(areas):
        areas[name.lower()] = areas[name]
        areas[areas[name]] = name

    print(areas)
