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
#   "search_str": string,
#   "breed": string
# }
def get_details_by_search(search_conditions: dict, pymongo_db: Database) -> List[Dog]:
    return []


def get_details_by_id(id: str, pymongo_db: Database):
    raise NotImplementedError
