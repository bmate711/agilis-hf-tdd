from .model import Dog

class ValidationKeyError(KeyError):
    pass

class ValidationError(Exception):
    pass

# Adatbázisban tárolni kell az új kutyákat
# A kutya neve nem tartalmazhatja a 'cat' szót
# Ha a kutya fiú 'M' kell kezdődni a neve
# Ha a kutya 5 évnél idősebb, rendelkezni kell 'cuteness' oltással
# Ha a kutya keverék, akkor szerepelnie kell a nevében 'Snow' szónak
# A leírás 50-100 karakte hosszú lehet
# A kutya színének szerepelnie kell a leírásban
def import_data(raw, db):
    for dog in raw:
        validate_dog_name(dog)
        validate_vaccination(dog)
        validate_description(dog)
    dogs = []
    for dog in raw:
        dogs.append(Dog(**dog).to_bson())
    db.insert_many(dogs)
    return True

def validate_dog_name(dog):
    if "cat" in dog["name"]:
        raise ValidationError("Name contain 'cat'")
    if dog["sex"] == True and dog["name"][0] != 'M':
        raise ValidationError("Male name should start with M")
    if dog["breed"] == "mixed":
        if "Snow" not in dog["name"]:
            raise ValidationError("Mixed breed dog name should contain 'Snow'")
    return dog

def validate_vaccination(dog):
    if dog["age"] > 5 and "cutness" not in dog["vaccination"]:
        raise ValidationError("Older than 5 should be vaccinated with cutness")

def validate_description(dog):
    if len(dog["description"]) < 50:
        raise ValidationError("Description should be longer than 50")
    if len(dog["description"]) > 100:
        raise ValidationError("Description should be shorter than 100")
    if dog["color"] not in dog["description"]:
        raise ValidationError("Description should contain dog color")

    




