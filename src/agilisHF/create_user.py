from agilisHF.objectid import PydanticObjectId
from .model import User
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex2 = r'^[a-zA-Z]+" "[a-zA-Z]+$'
# regex3 = r'\b[0-9]{9}+[A-Z]{2}\b'
regex3 = r'[0-9]{9}[A-Z]{2}'

class ValidationKeyError(KeyError):
    pass

class ValidationError(Exception):
    pass

def create_user(raw, db):
    validate_data(raw, db)
    save_user(raw, db)
    return True

def validate_data(raw, db):
    validate_fullname(raw)
    validate_idcardnumber(raw)
    validate_emailaddress(raw, db)
    validate_password(raw)

def save_user(raw, db):
    user = User(**raw)
    insert_result = db.insert_one(user.to_bson())
    user.id = PydanticObjectId(str(insert_result.inserted_id))
    return user

def validate_fullname(raw):
    fullname = raw["fullname"]
    if len(fullname) <= 2 or len(fullname) > 128:
        raise ValidationError("Invalid name, a name length should be between 2 and 128") 
    if (re.fullmatch(regex2, fullname)):
        raise ValidationError("Invalid name, must contain a first name and a last name and can't contain numbers")

def validate_idcardnumber(raw):
    idcardnumber = raw["idcardnumber"]
    if len(idcardnumber) != 11:
        raise ValidationError("ID must be 11 character")
    if type(idcardnumber) is not str:
        raise ValidationError("Idcardnumber value must be a valid string")
    if (not re.fullmatch(regex3, idcardnumber)):
        raise ValidationError("ID must in correct format 9 number then 2 character A-Z")


def validate_emailaddress(raw, db):
    email = raw['emailaddress']
    if(not re.fullmatch(regex, email)):
        raise ValidationError("Invalid email form")
    users=db.users
    existing_user=users.find_one({"emailadress":email})
    if not existing_user is None :
        raise ValidationError("Email address is already exist")

def validate_password(raw):
    password =  raw['password']
    if not re.search('[A-Z]', password) or not re.search('[0-9]', password):
        raise ValidationError("It must contain capital letter, and number")

    



