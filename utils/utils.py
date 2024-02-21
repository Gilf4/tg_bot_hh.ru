

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