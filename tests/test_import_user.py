from agilisHF.import_user import import_data
import mongomock 
import unittest
from agilisHF.import_user import ValidationError
from agilisHF.model import User

class DetailsTest(unittest.TestCase):
    db = mongomock.MongoClient().db.user

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        self.db.drop()
        return super().tearDown()

    def test_import_data_return_value_true(self):
        raw=[{'fullname':'Test Name','idcardnumber':'123456789AB','emailaddress':'asdika@pls.com','password':'#Artirw213'}]

        result = import_data(raw, self.db)
        assert True == result


    def test_import_data_user_name_must_contain_space(self):
        raw=[{'fullname':'TestName','idcardnumber':'123456789AB','emailaddress':'asdika@pls.com','password':'#Artirw213'}]
        with self.assertRaises(ValidationError) as context:
            result = import_data(raw, self.db)
        self.assertTrue("Name doesn't contain space character" in str(context.exception))


    def test_import_data_user_name_must_be_longer_than_two_character(self):
        raw=[{'fullname':'T ','idcardnumber':'123456789AB','emailaddress':'asdika@pls.com','password':'#Artirw213'}]
        with self.assertRaises(ValidationError) as context:
            result = import_data(raw, self.db)
        self.assertTrue("Name is shorter than two character" in str(context.exception))

    def test_import_data_user_name_must_be_shorter_than_128_character(self):
        raw=[{'fullname':'ABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEF ABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEF','idcardnumber':'123456789AB','emailaddress':'asdika@pls.com','password':'#Artirw213'}]
        with self.assertRaises(ValidationError) as context:
            result = import_data(raw, self.db)
        self.assertTrue("Name is longer than 128 character" in str(context.exception))

    def test_import_data_user_emailaddress_must_be_in_correct_format(self):
        raw=[{'fullname':'Test Name','idcardnumber':'123456789AB','emailaddress':'asdikaplscom','password':'#Artirw213'}]
        with self.assertRaises(ValidationError) as context:
            result = import_data(raw, self.db)
        self.assertTrue("Email must be in a correct email format" in str(context.exception))

    def test_import_data_user_idcardnumber_must_be_11_character(self):
        raw=[{'fullname':'Test Name','idcardnumber':'123452131231231236789AB','emailaddress':'asdika@pls.com','password':'#Artirw213'}]
        with self.assertRaises(ValidationError) as context:
            result = import_data(raw, self.db)
        self.assertTrue("ID must be 11 character" in str(context.exception))

    def test_import_data_user_idcardnumber_must_be_in_correct_format(self):
        raw=[{'fullname':'Test Name','idcardnumber':'123456AB789','emailaddress':'asdika@pls.com','password':'#Artirw213'}]
        with self.assertRaises(ValidationError) as context:
            result = import_data(raw, self.db)
        self.assertTrue("ID must in correct format 9 number then 2 character A-Z" in str(context.exception))
    

    def test_import_data_user_password_must_contain_capital_letter_and_number(self):
        raw=[{'fullname':'Test Name','idcardnumber':'123456AB789','emailaddress':'asdika@pls.com','password':'asdikaplusone'}]
        with self.assertRaises(ValidationError) as context:
            result = import_data(raw, self.db)
        self.assertTrue("Password must contain capital letter and number" in str(context.exception))
    