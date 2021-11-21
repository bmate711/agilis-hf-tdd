from agilisHF.import_dogs import import_data
import mongomock
import pytest
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

    def test_import_data_return_value_true(self):
        raw = [{'name': 'test', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'finally!!', 'vaccination': ['v1!!', 'vocid', 'cutness'], 'age': 10, 'sex': False}]
        result = import_data(raw, self.db)
        assert True == result

    def test_import_data_dog_exception_name_must_not_contain_cat(self):
        raw = [{'name': 'tecatst', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'finally!!', 'vaccination': ['v1!!', 'vocid', 'cutness'], 'age': 10, 'sex': False}]
        with pytest.raises(ValidationError):
            import_data(raw, self.db)