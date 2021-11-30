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



def get_details_by_search(search_conditions: dict, pymongo_db: Database) -> List[Dog]:
    dogs = pymongo_db.dogs
    validate_search_conditons(search_conditions)
    search_values = {}
    for key, value in search_conditions.items():
        if key == "search_str":
            pass
        if key == "vaccinated":
            search_values["vaccination"] = (
                {"$exists": True, "$ne": []}
                if value == True
                else {"$exists": True, "$eq": []}
            )
        elif value is not None:
            search_values[key] = value

    result = dogs.find(search_values)
    result_dogs = []
    if result.count() == 0 and len(search_values.keys()) != 0:
        if "search_str" not in search_conditions.keys():
            return []
        search_dogs = dogs.find()
        for dog in search_dogs:
            if (
                (dog["description"].find(search_conditions["search_str"]) > -1)
                or (dog["name"].find(search_conditions["search_str"]) > -1)
                or (dog["breed"].find(search_conditions["search_str"]) > -1)
            ):
                result_dogs.append(Dog(**dog))
        return result_dogs
    for dog in result:
        result_dogs.append(Dog(**dog))
    return result_dogs


valid_keys = ["name", "age", "vaccinated", "color", "sex", "breed"]
def validate_search_conditons(search_conditions: dict):
    validate_search_condition_keys(search_conditions)
    validate_search_condition_types(search_conditions)

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
    dogs = pymongo_db.dogs
    validate_id(id)
    dog = dogs.find_one({"_id": ObjectId(id)})
    if dog is not None:
        return Dog(**dog)
    return {}


def get_details_by_free_text(search_value: str, pymongo_db: Database):
    validate_search_string(search_value)
    dogs = pymongo_db.dogs.find()
    result: List[Dog] = []
    for dog_data in dogs:
        dog = Dog(**dog_data)
        if (
            (dog.description.find(search_value) > -1)
            or (dog.name.find(search_value) > -1)
            or (dog.breed.find(search_value) > -1)
        ):
            result.append(dog)
    return result


def validate_search_string(search_value: str):
    if type(search_value) is not str or (
        type(search_value) is str and len(search_value) == 0
    ):
        raise ValidationError(f"Search value should be a non empty string")


def validate_id(id: str):
    if type(id) is not str or (type(id) is str and len(id) == 0):
        raise ValidationError(f"Search value should be a non empty string")