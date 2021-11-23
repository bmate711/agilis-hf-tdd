from agilisHF.controllers import get_details_by_search
import mongomock
import unittest
from agilisHF.model import Dog


class DetailsTest(unittest.TestCase):
    db = mongomock.MongoClient().db.dogs
    dogs = [
        Dog(
            **{
                "name": "Test",
                "color": "white",
                "breed": "husky",
                "age": 1,
                "vaccination": [],
                "sex": True,
                "description": "Teszt",
            }
        ),
        Dog(
            **{
                "name": "Test2",
                "color": "white",
                "breed": "husky",
                "age": 5,
                "vaccination": ["covid19", "covid21"],
                "sex": True,
                "description": "Teszt",
            }
        ),
        Dog(
            **{
                "name": "Test3",
                "color": "white",
                "breed": "husky",
                "age": 5,
                "vaccination": [],
                "sex": True,
                "description": "Teszt",
            }
        ),
    ]

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        self.db.drop()
        return super().tearDown()

    def test_parameter_not_null_and_not_throwing(self):
        get_details_by_search({"name": "Doggo", "age": 22}, self.db)
