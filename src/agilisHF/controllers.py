from os import name
from typing import List
from bson.objectid import ObjectId
from flask.json import jsonify
from flask_pymongo.wrappers import Database

from agilisHF.model import Dog


class SearchKeyError(KeyError):
    pass


class ValidationError(Exception):
    pass


# Search conditions
# { "name": string
#   "age": number,
#   "vaccinated": boolean
#   "color": string
#   "sex": boolean
#   "breed": string
# }
def get_details_by_search(search_conditions: dict, pymongo_db: Database) -> List[Dog]:
    validate_search_condition_keys(search_conditions)
    validate_search_condition_types(search_conditions)
    result = pymongo_db.dogs.find(search_conditions)
    dogs: List[Dog] = []
    for dog in result:
        dogData = Dog(**dog)
        dogs.append(dogData)
    return dogs


valid_keys = ["name", "age", "vaccinated", "color", "sex", "breed"]


def validate_search_condition_keys(search_conditions: dict):
    for key in search_conditions.keys():
        if key not in valid_keys:
            raise ValidationError(f"Wrong key in search condition: {key}")


string_keys = ["name", "color", "breed"]
bool_keys = ["vaccinated", "sex"]
int_keys = ["age"]


def validate_search_condition_types(search_conditions: dict):
    for key in search_conditions.keys():
        if key in string_keys and type(search_conditions[key]) is not str:
            raise ValidationError(f"{key} should be a non empty string")
        if key in bool_keys and type(search_conditions[key]) is not bool:
            raise ValidationError(f"{key} should be a bool")
        if key in int_keys and type(search_conditions[key]) is not int:
            raise ValidationError(f"{key} should be an integer")


def get_details_by_id(id: str, pymongo_db: Database):
    raise NotImplementedError
