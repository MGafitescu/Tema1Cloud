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

@db_session
def get_dinos_by_period(period_id):
    dinos = []
    try:
        period = models.Period[period_id]
        for dino in period.dinosaurs:
            dino_view = views.DinosaurView()
            dino_view.name = dino.name
            dino_view.length = dino.length
            dino_view.weight = dino.weight
            dino_view.period = dino.period.name
            dino_view.dinosaur_type = dino.type.name
            dino_view.diet = dino.diet
            dino_view.id = dino.id
            dinos.append(dino_view)
    except ObjectNotFound:
        return None
    return dinos

@db_session
def get_dinos_by_type(type_id):
    dinos = []
    try:
        type = models.Type[type_id]
        for dino in type.dinosaurs:
            dino_view = views.DinosaurView()
            dino_view.name = dino.name
            dino_view.length = dino.length
            dino_view.weight = dino.weight
            dino_view.period = dino.period.name
            dino_view.dinosaur_type = dino.type.name
            dino_view.diet = dino.diet
            dino_view.id = dino.id
            dinos.append(dino_view)
    except ObjectNotFound:
        return None

    return dinos



models.generate_mappings()

if __name__ == "__main__":
    types = [None, None, None]
    types[0] = views.TypeView("Sauropod", "Sauropoda", "Very large herbivores that walked mostly on four legs.")
    types[1] = views.TypeView("Theropod", "Theropoda", "Large carnivores that walked on two legs.")
    types[2] = views.TypeView("Armoured dinosaurs", "Ankylosauria",
                              "Medium-sized, four-legged herbivores with body armour, sometimes including tail spikes.")
    for type in types:
        add_type(type)
    periods = [None, None, None, None]
    periods[0] = views.PeriodView("Late Cretaceous", 101.5, 66, "Second part of Cretaceous")
    periods[1] = views.PeriodView("Early Cretaceous", 145, 101.5, "First part of Cretaceous")
    periods[2] = views.PeriodView("Early Jurassic", 201, 174, "First part of Jurassic")
    periods[3] = views.PeriodView("Late Triassic", 237, 201, "First dinosaurs")
    for period in periods:
        add_period(period)
    dinos = [None, None, None, None, None, None]
    dinos[0] = views.DinosaurView("Iguanodon", 3, 10, 4000, 2, "herbivorous")
    dinos[1] = views.DinosaurView("Fukuiraptor", 2, 4.2, 1000, 2, "carnivorous")
    dinos[2] = views.DinosaurView("Vulcanodon", 1, 6.5, 3000, 3, "herbivorous")
    dinos[3] = views.DinosaurView("Eoraptor", 2, 1, 200, 4, "carnivorous")
    dinos[4] = views.DinosaurView("Futalognksosaurus", 1, 32, 70000, 1, "herbivorous")
    dinos[5] = views.DinosaurView("Pentaceraptos", 3, 6.8, 2500, 1, "herbivorous")
    for dino in dinos:
        add_dino(dino)
