import mongomock
import unittest
from agilisHF.controllers import ValidationError, get_details_by_search
from agilisHF.model import Dog

class DetailsTest(unittest.TestCase):
    db = mongomock.MongoClient().db

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        self.db.dogs.drop()
        return super().tearDown()