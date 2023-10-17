#!/usr/bin/python3
"""
Defines unittests for models/base_model.py.
Unittest classes:
    TestBaseModelInstantiation
    TestBaseModelSave
    TestBaseModelToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModelInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def setUp(self):
        """Set up a test instance."""
        self.bm = BaseModel()

    def test_no_args_instantiates(self):
        """Test if BaseModel can be instantiated with no arguments."""
        self.assertIsInstance(self.bm, BaseModel)

    def test_new_instance_stored_in_objects(self):
        """
        Test if a new instance of BaseModel is stored in the objects dictionary
        """
        self.assertIn(self.bm, models.storage.all().values())

    def test_id_is_public_str(self):
        """Test if 'id' attribute is a public string."""
        self.assertIsInstance(self.bm.id, str)

    def test_created_at_is_public_datetime(self):
        """Test if 'created_at' attribute is a public datetime object."""
        self.assertIsInstance(self.bm.created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        """Test if 'updated_at' attribute is a public datetime object."""
        self.assertIsInstance(self.bm.updated_at, datetime)

    def test_two_models_unique_ids(self):
        """Test if two BaseModel instances have unique IDs."""
        bm2 = BaseModel()
        self.assertNotEqual(self.bm.id, bm2.id)

    def test_two_models_different_created_at(self):
        """
        Test if two BaseModel instances have different 'created_at' values.
        """
        sleep(0.05)
        bm2 = BaseModel()
        self.assertLess(self.bm.created_at, bm2.created_at)

    def test_two_models_different_updated_at(self):
        """
        Test if two BaseModel instances have different 'updated_at' values.
        """
        sleep(0.05)
        bm2 = BaseModel()
        self.assertLess(self.bm.updated_at, bm2.updated_at)

    def test_str_representation(self):
        """Test the string representation of BaseModel."""
        dt = datetime.today()
        dt_repr = repr(dt)
        self.bm.id = "123456"
        self.bm.created_at = self.bm.updated_at = dt
        expected_output = f"[BaseModel] (123456) {self.bm.__dict__}"
        self.assertEqual(str(self.bm), expected_output)

    def test_args_unused(self):
        """Test if BaseModel ignores unused arguments."""
        self.bm = BaseModel(None)
        self.assertNotIn(None, self.bm.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation of BaseModel with keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """
        Test if BaseModel raises an error when instantiated
        with None keyword arguments.
        """
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        """
        Test instantiation of BaseModel with both positional
        and keyword arguments.
        """
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)


class TestBaseModelSave(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    def setUp(self):
        """Set up a test instance."""
        self.bm = BaseModel()

    @classmethod
    def tearDownClass(cls):
        """Clean up the class-level setup."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_one_save(self):
        """Test if saving the BaseModel updates 'updated_at' attribute."""
        sleep(0.05)
        first_updated_at = self.bm.updated_at
        self.bm.save()
        self.assertLess(first_updated_at, self.bm.updated_at)

    def test_two_saves(self):
        """
        Test if saving the BaseModel multiple times updates
        the 'updated_at' attribute.
        """
        sleep(0.01)
        first_updated_at = self.bm.updated_at
        self.bm.save()
        second_updated_at = self.bm.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.01)
        self.bm.save()
        self.assertLess(second_updated_at, self.bm.updated_at)

    def test_save_with_arg(self):
        """Test if saving the BaseModel with an argument raises a TypeError."""
        with self.assertRaises(TypeError):
            self.bm.save(None)

    def test_save_updates_file(self):
        """Test if saving the BaseModel updates the 'file.json' file."""
        self.bm.save()
        bmid = f"BaseModel.{self.bm.id}"
        with open("file.json", "r") as file:
            self.assertIn(bmid, file.read())


class TestBaseModelToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def setUp(self):
        """Set up a test instance."""
        self.bm = BaseModel()

    def tearDown(self):
        """Clean up the file created by the test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_to_dict_type(self):
        """Test the data type of the to_dict method's return value."""
        self.assertIsInstance(self.bm.to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        """Test if the keys in the to_dict method's return value are correct"""
        self.assertIn("id", self.bm.to_dict())
        self.assertIn("created_at", self.bm.to_dict())
        self.assertIn("updated_at", self.bm.to_dict())
        self.assertIn("__class__", self.bm.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test if added attributes are included in the to_dict return value"""
        self.bm.name = "ALXSE"
        self.bm.my_number = 98
        self.assertIn("name", self.bm.to_dict())
        self.assertIn("my_number", self.bm.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """
        Test if 'created_at' and 'updated_at' in the to_dict
        return value are strings.
        """
        bm_dict = self.bm.to_dict()
        self.assertIsInstance(bm_dict["created_at"], str)
        self.assertIsInstance(bm_dict["updated_at"], str)

    def test_to_dict_output(self):
        """Test the output of the to_dict method with sample data."""
        dt = datetime.today()
        self.bm.id = "123456"
        self.bm.created_at = self.bm.updated_at = dt
        expected_output = {
            "id": "123456",
            "__class__": "BaseModel",
            "created_at": dt.isoformat(),
            "updated_at": dt.isoformat(),
        }
        self.assertEqual(self.bm.to_dict(), expected_output)

    def test_contrast_to_dict_dunder_dict(self):
        """
        Test if the to_dict method output is different from the __dict__ attr.
        """
        self.assertNotEqual(self.bm.to_dict(), self.bm.__dict__)

    def test_to_dict_with_arg(self):
        """
        Test if calling to_dict method with an argument raises a TypeError.
        """
        with self.assertRaises(TypeError):
            self.bm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
