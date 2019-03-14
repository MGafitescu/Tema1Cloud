class DinosaurView:
    def __init__(self, name=None, dinosaur_type=None, length=None, weight=None, period=None, diet=None):
        self.name = name
        self.dinosaur_type = dinosaur_type
        self.length = length
        self.weight = weight
        self.diet = diet
        self.period = period

    def to_dict(self):
        return self.__dict__

    def from_dict(self, dino_dict):
        self.name = dino_dict.get("name", None)
        self.dinosaur_type = dino_dict.get("dinosaur_type", None)
        self.length = dino_dict.get("length", None)
        self.weight = dino_dict.get("weight", None)
        self.diet = dino_dict.get("diet", None)
        self.period = dino_dict.get("period", None)


class PeriodView:
    def __init__(self, name=None, start=None, end=None, description=None):
        self.name = name
        self.start = start
        self.end = end
        self.description = description

    def to_dict(self):
        return self.__dict__

    def from_dict(self, period_dict):
        self.name = period_dict.get("name", None)
        self.start = period_dict.get("start", None)
        self.end = period_dict.get("end", None)
        self.description = period_dict.get("description", None)


class TypeView:
    def __init__(self, name=None, taxonomy=None, characteristics=None):
        self.name = name
        self.characteristics = characteristics
        self.taxonomy = taxonomy

    def to_dict(self):
        return self.__dict__

    def from_dict(self, type_dict):
        self.name = type_dict.get("name", None)
        self.taxonomy = type_dict.get("taxonomy", None)
        self.characteristics = type_dict.get("characteristics", None)
