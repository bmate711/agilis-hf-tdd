from agilisHF.import_dogs import import_data
import mongomock 
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
        self.assertTrue("Male name should start with M" in str(context.exception))

    def test_import_data_older_than_5_cutness_needed(self):
        raw = [{'name': 'test', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'finally!!', 'vaccination': ['v1!!', 'vocid'], 'age': 10, 'sex': False}]
        with self.assertRaises(ValidationError) as context:
            import_data(raw, self.db)
        self.assertTrue("Older than 5 should be vaccinated with cutness" in str(context.exception))


    def test_import_data_mixed_breed_name_contain_snow(self):
        raw = [{'name': 'test', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'mixed', 'vaccination': ['v1!!', 'vocid', 'cutness'], 'age': 10, 'sex': False}]
        with self.assertRaises(ValidationError) as context:
            import_data(raw, self.db)
        self.assertTrue("Mixed breed dog name should contain 'Snow'" in str(context.exception))

    def test_import_data_exception_description_sorter_than_50(self):
        raw = [{'name': 'Mtest', 'color': 'brown', 'description': 'description!! brown', 'breed': 'mixed', 'vaccination': ['v1!!', 'vocid'], 'age': 1, 'sex': True}]
        with self.assertRaises(ValidationError) as context:
            import_data(raw, self.db)
        self.assertTrue("Description should be longer than 50" in str(context.exception))

    def test_import_data_exception_description_onger_than_100(self):
        raw = [{'name': 'Mtest', 'color': 'brown', 'description': 'description!! brown ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd', 'breed': 'mixed', 'vaccination': ['v1!!', 'vocid'], 'age': 1, 'sex': True}]
        with self.assertRaises(ValidationError) as context:
            import_data(raw, self.db)
        self.assertTrue("Description should be shorter than 100" in str(context.exception))
