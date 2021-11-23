from agilisHF.controllers import (
    ValidationError,
    get_details_by_free_text,
    get_details_by_id,
    get_details_by_search,
)
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

    ids = []

    def setUp(self) -> None:
        for dog in self.dogs:
            d = self.db.dogs.insert_one(dog.to_bson())
            self.ids.append(str(d.inserted_id))
        return super().setUp()

    def tearDown(self) -> None:
        self.db.dogs.drop()
        self.ids = []
        return super().tearDown()

    def test_parameter_not_null_and_not_throwing(self):
        get_details_by_search({"name": "Doggo", "age": 22}, self.db)

    def test_good_query_should_return_dog_list(self):
        result = get_details_by_search({"name": "Test", "age": 1}, self.db)
        assert len(result) == 1

    def test_wrong_params_throw_validation_error(self):
        with self.assertRaises(ValidationError):
            get_details_by_search({"test": "test", "null": None}, self.db)

    def test_wrong_param_type_throw_validation_error(self):
        with self.assertRaises(ValidationError):
            get_details_by_search(
                {"name": 1, "age": "Middle age", "sex": "male"}, self.db
            )

    def test_vaccinated_value_should_work_with_false(self):
        result = get_details_by_search(
            {"name": "Test", "age": 1, "vaccinated": False}, self.db
        )
        assert len(result) == 1
        assert result[0].name == self.dogs[0].name
        # Does not have vaccine
        assert len(result[0].vaccination) == 0

    def test_vaccinated_value_should_work_with_true(self):
        result = get_details_by_search(
            {"name": "Test", "age": 1, "vaccinated": False}, self.db
        )
        assert len(result) == 1
        assert result[0].name == self.dogs[0].name
        # Does not have vaccine
        assert len(result[0].vaccination) == 0

    def test_search_by_free_text_should_not_throw_with_params(self):
        get_details_by_free_text("Teszt", self.db)

    def test_search_by_free_text_should_return_value(self):
        result = get_details_by_free_text("Teszt", self.db)
        assert result[0].name == self.dogs[0].name

    def test_search_by_free_text_should_throw_validation_error(self):
        with self.assertRaises(ValidationError):
            get_details_by_free_text(0, self.db)

    def test_search_by_id_should_not_throw_with_params(self):
        get_details_by_id(self.ids[0], self.db)

    def test_search_by_id_should_throw_validation_error(self):
        with self.assertRaises(ValidationError):
            get_details_by_id(0, self.db)
