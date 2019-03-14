import repository
import json
import views


def get_periods():
    period_list = repository.get_periods()
    if len(period_list) == 0:
        response = 204
        content = ''
        content_type = "text/html"
    else:
        period_list = [x.to_dict() for x in period_list]
        content = json.dumps(period_list)
        response = 200
        content_type = "application/json"
    return response, content, content_type


def get_period(period_id):
    period = repository.get_period(period_id)
    if period is None:
        content = "The resource required does not exist"
        content_type = "text/html"
        response = 404
    else:
        period = period.to_dict()
        content = json.dumps(period)
        response = 200
        content_type = "application/json"
    return response, content, content_type


def add_period(payload):
    period = views.PeriodView()
    period.from_dict(payload)
    if period.name is None or period.start is None or period.end is None:
        return 400, "Missing fields", "text/html"
    try:
        period.start = float(period.start)
        period.end = float(period.end)
    except ValueError:
        return 422, "Start and end should be floats", "text/html"
    if period.start < period.end:
        return 422, "Start date should be higher than end date( million years ago)", "text/html"
    if period.description is None:
        period.description = "No description available"

    response = repository.add_period(period)
    if response == -1:
        return 409, "Conflict: period with same name already exists", "text/html"
    return 201, str(response), "text/html"


def update_period(payload, id):
    period = views.PeriodView()
    period.from_dict(payload)
    if period.name is None or period.start is None or period.end is None:
        return 400, "Missing fields", "text/html"
    try:
        period.start = float(period.start)
        period.end = float(period.end)
    except ValueError:
        return 422, "Start and end should be floats", "text/html"
    if period.start < period.end:
        return 422, "Start date should be higher than end date( million years ago)", "text/html"
    if period.description is None:
        period.description = "No description available"
    try:
        id = int(id)
    except ValueError:
        return 400, "Id is not integer", "text/html"

    response = repository.update_period(period, id)
    if response is True:
        return 200, "", "text/html"
    elif response is False:
        return 409, "Conflict: period with same name already exists", "text/html"
    else:
        return 201, str(response), "text/html"


def delete_period(id):
    try:
        id = int(id)
    except ValueError:
        return 400, "Id is not integer", "text/html"
    response = repository.delete_period(id)
    if response is True:
        return 200, '', 'text/html'
    return 404, 'Resource not found', 'text/html'


def get_types():
    types_list = repository.get_types()
    if len(types_list) == 0:
        response = 204
        content = ''
        content_type = "text/html"
    else:
        types_list = [x.to_dict() for x in types_list]
        content = json.dumps(types_list)
        response = 200
        content_type = "application/json"
    return response, content, content_type


def get_type(type_id):
    type = repository.get_period(type_id)
    if type is None:
        content = "The resource required does not exist"
        content_type = "text/html"
        response = 404
    else:
        type = type.to_dict()
        content = json.dumps(type)
        response = 200
        content_type = "application/json"
    return response, content, content_type


def add_type(payload):
    type = views.TypeView()
    type.from_dict(payload)
    if type.name is None or type.taxonomy is None or type.characteristics is None:
        return 400, "Missing fields", "text/html"
    response = repository.add_type(type)
    if response == -1:
        return 409, "Conflict: type with same name already exists", "text/html"
    return 201, str(response), "text/html"


def update_type(payload, id):
    type = views.TypeView()
    type.from_dict(payload)
    if type.name is None or type.taxonomy is None or type.characteristics is None:
        return 400, "Missing fields", "text/html"
    try:
        id = int(id)
    except ValueError:
        return 400, "Id is not integer", "text/html"

    response = repository.update_type(type, id)
    if response is True:
        return 200, "", "text/html"
    elif response is False:
        return 409, "Conflict: type with same name already exists", "text/html"
    else:
        return 201, str(response), "text/html"


def delete_type(id):
    try:
        id = int(id)
    except ValueError:
        return 400, "Id is not integer", "text/html"
    response = repository.delete_type(id)
    if response is True:
        return 200, '', 'text/html'
    return 404, 'Resource not found', 'text/html'


def get_dinos():
    dino_list = repository.get_dinos()
    if len(dino_list) == 0:
        response = 204
        content = ''
        content_type = "text/html"
    else:
        dino_list = [x.to_dict() for x in dino_list]
        content = json.dumps(dino_list)
        response = 200
        content_type = "application/json"
    return response, content, content_type


def get_dino(dino_id):
    dino = repository.get_dino(dino_id)
    if dino is None:
        content = "The resource required does not exist"
        content_type = "text/html"
        response = 404
    else:
        dino = dino.to_dict()
        content = json.dumps(dino)
        response = 200
        content_type = "application/json"
    return response, content, content_type


def add_dino(payload):
    dino = views.DinosaurView()
    dino.from_dict(payload)
    if dino.name is None or dino.length is None or dino.weight is None \
            or dino.dinosaur_type is None or dino.period is None:
        return 400, "Missing fields", "text/html"
    if dino.diet is None:
        dino.diet = "No diet data available"
    period_view = repository.get_period_by_name(dino.period)
    if period_view is None:
        return 422, "Period does not exist", "text/html"
    dino.period = period_view.id
    type_view = repository.get_type_by_name(dino.dinosaur_type)
    if type_view is None:
        return 422, "Type does not exist", "text/html"
    dino.dinosaur_type = type_view.id
    try:
        dino.weight = int(dino.weight)
        dino.length = float(dino.length)
    except ValueError:
        return 422, "Weight should be int and length should be float", "text/html"

    response = repository.add_dino(dino)
    if response == -1:
        return 409, "Conflict: period with same name already exists", "text/html"
    return 201, str(response), "text/html"


def update_dino(payload, id):
    dino = views.DinosaurView()
    dino.from_dict(payload)
    if dino.name is None or dino.length is None or dino.weight is None \
            or dino.dinosaur_type is None or dino.period is None:
        return 400, "Missing fields", "text/html"
    if dino.diet is None:
        dino.diet = "No diet data available"
    period_view = repository.get_period_by_name(dino.period)
    if period_view is None:
        return 422, "Period does not exist", "text/html"
    dino.period = period_view.id
    type_view = repository.get_type_by_name(dino.dinosaur_type)
    if type_view is None:
        return 422, "Type does not exist", "text/html"
    dino.dinosaur_type = type_view.id
    try:
        dino.weight = int(dino.weight)
        dino.length = float(dino.length)
    except ValueError:
        return 422, "Weight should be int and length should be float", "text/html"
    try:
        id = int(id)
    except ValueError:
        return 400, "Id is not integer", "text/html"

    response = repository.update_dino(dino, id)
    if response is True:
        return 200, "", "text/html"
    elif response is False:
        return 409, "Conflict: period with same name already exists", "text/html"
    else:
        return 201, str(response), "text/html"


def delete_dino(id):
    try:
        id = int(id)
    except ValueError:
        return 400, "Id is not integer", "text/html"
    response = repository.delete_dino(id)
    if response is True:
        return 200, '', 'text/html'
    return 404, 'Resource not found', 'text/html'
