from pony.orm import *
import models
import views


@db_session
def add_type(type_view):
    dino_type = models.Type(name=type_view.name, taxonomy=type_view.taxonomy,
                            characteristics=type_view.characteristics)
    try:
        commit()
        return dino_type.id
    except TransactionIntegrityError:
        return -1


@db_session
def get_types():
    types = []
    for dino_type in models.Type.select():
        type_view = views.TypeView(dino_type.name, dino_type.taxonomy, dino_type.characteristics)
        type_view.id = dino_type.id
        types.append(type_view)
    return types


@db_session
def get_type(type_id):
    try:
        dino_type = models.Type[type_id]
        type_view = views.TypeView(dino_type.name, dino_type.taxonomy, dino_type.characteristics)
        type_view.id = dino_type.id
    except ObjectNotFound:
        type_view = None
    return type_view


@db_session
def get_type_by_name(name):
    dino_type = models.Type.get(name=name)
    if dino_type is not None:
        type_view = views.TypeView(dino_type.name, dino_type.taxonomy, dino_type.characteristics)
        type_view.id = dino_type.id
        return type_view
    else:
        return None


@db_session
def update_type(type_view, type_id):
    try:
        dino_type = models.Type[type_id]
        dino_type.name = type_view.name
        dino_type.taxonomy = type_view.taxonomy
        dino_type.characteristics = type_view.characteristics
        commit()
        return True
    except ObjectNotFound:
        dino_type = models.Type(id=type_id, name=type_view.name, taxonomy=type_view.taxonomy,
                                characteristics=type_view.characteristics)
        try:
            commit()
            return dino_type.id
        except TransactionIntegrityError:
            return False
    except IntegrityError:
        return False


@db_session
def delete_type(type_id):
    try:
        models.Type[type_id].delete()
        commit()
        return True
    except ObjectNotFound:
        return False


@db_session
def add_period(period_view):
    period = models.Period(name=period_view.name, start=period_view.start, end=period_view.end
                           , description=period_view.description)
    try:
        commit()
        return period.id
    except TransactionIntegrityError:
        return -1


@db_session
def get_periods():
    periods = []
    for period in models.Period.select():
        period_view = views.PeriodView(period.name, period.start, period.end, period.description)
        period_view.id = period.id
        periods.append(period_view)
    return periods


@db_session
def get_period(period_id):
    try:
        period = models.Period[period_id]
        period_view = views.PeriodView(period.name, period.start, period.end, period.description)
        period_view.id = period.id
    except ObjectNotFound:
        period_view = None
    return period_view


@db_session
def get_period_by_name(name):
    period = models.Period.get(name=name)
    if period is not None:
        period_view = views.PeriodView(period.name, period.start, period.end, period.description)
        period_view.id = period.id
        return period_view
    else:
        return None


@db_session
def update_period(period_view, period_id):
    try:
        period = models.Period[period_id]
        period.name = period_view.name
        period.start = period_view.start
        period.end = period_view.end
        period.description = period_view.description
        commit()
        return True
    except ObjectNotFound:
        period = models.Period(name=period_view.name, start=period_view.start, end=period_view.end
                               , description=period_view.description)
        try:
            commit()
            return period.id
        except TransactionIntegrityError:
            return False
    except IntegrityError:
        return False


@db_session
def delete_period(period_id):
    try:
        models.Period[period_id].delete()
        commit()
        return True
    except ObjectNotFound:
        return False


@db_session
def get_dinos():
    dinos = []
    for dino in models.Dinosaur.select():
        dino_view = views.DinosaurView()
        dino_view.name = dino.name
        dino_view.length = dino.length
        dino_view.weight = dino.weight
        dino_view.period = dino.period.name
        dino_view.dinosaur_type = dino.type.name
        dino_view.diet = dino.diet
        dino_view.id = dino.id
        dinos.append(dino_view)
    return dinos


@db_session
def get_dino(dino_id):
    try:
        dino = models.Dinosaur[dino_id]
        dino_view = views.DinosaurView()
        dino_view.name = dino.name
        dino_view.length = dino.length
        dino_view.weight = dino.weight
        dino_view.period = dino.period.name
        dino_view.dinosaur_type = dino.type.name
        dino_view.diet = dino.diet
        dino_view.id = dino.id
    except ObjectNotFound:
        dino_view = None
    return dino_view


@db_session
def add_dino(dino_view):
    dino = models.Dinosaur(name=dino_view.name, length=dino_view.length, weight=dino_view.weight,
                           period=models.Period[dino_view.period],
                           type=models.Type[dino_view.dinosaur_type],
                           diet=dino_view.diet)
    try:
        commit()
        return dino.id
    except TransactionIntegrityError:
        return -1


@db_session
def update_dino(dino_view, dino_id):
    try:
        dino = models.Dinosaur[dino_id]
        dino.name = dino_view.name
        dino.length = dino_view.length
        dino.weight = dino_view.weight
        dino.period = models.Period[dino_view.period]
        dino.type = models.Type[dino_view.dinosaur_type]
        dino.diet = dino.diet
        commit()
        return True
    except ObjectNotFound:
        dino = models.Dinosaur(id=dino_id, name=dino_view.name, length=dino_view.length, weight=dino_view.weight,
                               period=models.Period[dino_view.period],
                               type=models.Type[dino_view.dinosaur_type],
                               diet=dino_view.diet)
        try:
            commit()
            return dino.id
        except TransactionIntegrityError:
            return False
    except IntegrityError:
        return False


@db_session
def delete_dino(dino_id):
    try:
        models.Dinosaur[dino_id].delete()
        commit()
        return True
    except ObjectNotFound:
        return False


models.generate_mappings()
