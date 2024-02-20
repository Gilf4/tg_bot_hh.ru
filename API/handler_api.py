import requests
from url_requests import *


def send_requests(url: str, par: dict = None) -> any:
    """
    :param url: url api
    :param par: options params
    :return: json request for url with params
    """

    req = requests.get(url, params=par)

    if req.status_code == 200:
        data = req.json()
        req.close()
        return data


def get_areas_json() -> any:
    """
    :return: returned json areas
    """

    return send_requests(url_get_areas)


def json_to_dict(areas_tree: any, areas: dict) -> None:
    for area in areas_tree:
        areas[area['name']] = area['id']

        if area.get('areas'):
            json_to_dict(area['areas'], areas)


def get_areas(is_smarted: bool = False):
    """
    :return: return dict {name: number name}
    :param is_smarted: is True return {number name: name}
    """

    areas_tree = get_areas_json()
    areas = {}
    json_to_dict(areas_tree, areas)

    if is_smarted:
        for name in list(areas):
            areas[name.lower()] = areas[name]
            areas[areas[name]] = name

    return areas


def main():
    data = get_areas(True)
    print(data)
    print(data.get('Нижний Новгород'))


if __name__ == '__main__':
    main()
