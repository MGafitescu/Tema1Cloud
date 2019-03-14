from pony.orm import *

db = Database()


class Dinosaur(db.Entity):
    name = Required(str, unique=True)
    type = Required('Type')
    length = Required(float)
    weight = Required(int)
    diet = Optional(str)
    period = Required('Period')


class Period(db.Entity):
    name = Required(str, unique=True)
    start = Required(float)
    end = Required(float)
    description = Optional(str)
    dinosaurs = Set(Dinosaur)


class Type(db.Entity):
    name = Required(str, unique=True)
    taxonomy = Required(str)
    characteristics = Required(str)
    dinosaurs = Set(Dinosaur)


def generate_mappings():
    db.bind(provider='sqlite', filename='database.db')
    db.generate_mapping(create_tables=True)

