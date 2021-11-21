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
    return True

    

    




