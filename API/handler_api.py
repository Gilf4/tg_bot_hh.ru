import requests
from api_requests import *


def send_requests(url: str, par: dict = None) -> any:
    """
    :param url: path to api
    :param par: options params
    :return: json request for path with params
    """

    req = requests.get(url, params=par)
    data = req.json()
    req.close()

    return data


def get_areas_tree() -> any:
    return send_requests(get_areas_api)


def pars_areas(areas_tree: any, areas: dict) -> None:
    for area in areas_tree:
        areas[area['name']] = area['id']

        if area.get('areas'):
            pars_areas(area['areas'], areas)


def get_areas(is_all: bool = False):
    """
    :return: return dict {name: number name}
    :param is_all: is True return {number name: name}
    """

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
