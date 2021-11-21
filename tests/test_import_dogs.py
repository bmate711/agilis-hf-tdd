from agilisHF.import_dogs import import_data
import mongomock
import pytest
import unittest
from agilisHF.import_dogs import ValidationError
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

    def test_import_data_dog_name_must_not_contain_cat(self):
        raw = [{'name': 'tecatst', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'finally!!', 'vaccination': ['v1!!', 'vocid', 'cutness'], 'age': 10, 'sex': False}]
        with self.assertRaises(ValidationError) as context:
            import_data(raw, self.db)
        self.assertTrue("Name contain 'cat'" in str(context.exception))

    def test_import_data_dog_male_name_should_start_with_M(self):
        raw = [{'name': 'sest', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'finally!!', 'vaccination': ['v1!!', 'vocid', 'cutness'], 'age': 10, 'sex': True}]
        with self.assertRaises(ValidationError) as context:
            import_data(raw, self.db)
        self.assertTrue("Name contain 'cat'" in str(context.exception))
