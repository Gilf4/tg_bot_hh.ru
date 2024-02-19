import requests
from api_requests import *


def get_areas_tree() -> any:
    req = requests.get(get_areas_api)
    data = req.json()
    req.close()

    return data


def pars_areas(areas_tree: any, areas: dict) -> None:
    for area in areas_tree:
        areas[area['name']] = area['id']

        if area.get('areas'):
            pars_areas(area['areas'], areas)


def get_areas(is_all: bool = False):
    areas_tree = get_areas_tree()
    areas = {}
    pars_areas(areas_tree, areas)

    if is_all:
        for name in list(areas):
            areas[areas[name]] = name

    return areas


def main():
    data = get_areas(True)
    print(data)
    print(data.get('Нижний Новгород'))


if __name__ == '__main__':
    main()
