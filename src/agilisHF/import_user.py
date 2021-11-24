from .model import User
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex2 = r'\b[A-Za-z]+" "+[A-Za-z]\b'
regex3 = r'\b[0-9]{9}+[A-Z]{2}\b'

class ValidationKeyError(KeyError):
    pass

class ValidationError(Exception):
    pass

def import_data(raw, db):
    for user in raw:
        validate_fullname(user)
        validate_idcardnumber(user)
        validate_emailaddress(user)
        validate_password(user)
    users = []
    for user in raw:
        users.append(User(**user).to_bson())
    db.insert_many(users)
    return True

def validate_fullname(raw):
   
    if (re.fullmatch(regex2, raw["name"])):
        raise ValidationError("Invalid name, must contain a first name and a last name and can't contain numbers")
    if len(raw["name"]) < 2 or len(raw["name"]) > 128:
        raise ValidationError("Invalid name, a name length should be between 2 and 128") 

def validate_idcardnumber(raw):
    if (re.fullmatch(regex3, raw["idcardnumber"])):
        raise ValidationError("ID card must be 11 character, the first 9 should be number and the last 2 should be letter")

def validate_emailaddress(raw, db):
    if(re.fullmatch(regex,raw['emailaddress'])):
        raise ValidationError("Invalid email form")
    users=db.users
    existing_user=users.find_one({"emailadress":raw['emailaddress']})
    if not existing_user is None :
        raise ValidationError("Email address is already exist")

def validate_password(raw):
    if not re.search('[A-Z]', raw['password']) or not re.search('[0-9]', raw['password']):
        raise ValidationError("It must contain capital letter, and number")

    



