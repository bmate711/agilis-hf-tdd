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
    return True

def validate_dog_name(dog):
    if "cat" in dog["name"]:
        raise ValidationError("Name contain 'cat'")
    if dog["sex"] == True and dog["name"] != 'M':
        raise ValidationError("Male name should start with M")
    return dog

def validate_vaccination(dog):
    if dog["age"] > 5 and "cutness" not in dog["vaccination"]:
        raise ValidationError("Older than 5 should be vaccinated with cutness")
    

    




