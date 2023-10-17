#!/usr/bin/python3
"""Defines unittests for models/place.py.
Unittest classes:
    TestPlaceInstantiation
    TestPlaceSave
    TestPlaceToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlaceInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    @classmethod
    def setUpClass(cls):
        """Set up the class for testing."""
        try:
            os.rename("file.json", "tmp")
        except FileNotFoundError:
            pass

    @classmethod
    def tearDownClass(cls):
        """Clean up after testing."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmp", "file.json")
        except FileNotFoundError:
            pass

    def test_instantiation(self):
        """Test basic instantiation of Place class."""
        place = Place()
        self.assertIsInstance(place, Place)
        self.assertIn(place, models.storage.all().values())
        self.assertIsInstance(place.id, str)
        self.assertIsInstance(place.created_at, datetime)
        self.assertIsInstance(place.updated_at, datetime)
        self.assertIsInstance(Place.city_id, str)
        self.assertIn("city_id", dir(place))
        self.assertNotIn("city_id", place.__dict__)
        self.assertIsInstance(Place.user_id, str)
        self.assertIn("user_id", dir(place))
        self.assertNotIn("user_id", place.__dict__)
        self.assertIsInstance(Place.name, str)
        self.assertIn("name", dir(place))
        self.assertNotIn("name", place.__dict__)
        self.assertIsInstance(Place.description, str)
        self.assertIn("description", dir(place))
        self.assertNotIn("description", place.__dict__)
        self.assertIsInstance(Place.number_rooms, int)
        self.assertIn("number_rooms", dir(place))
        self.assertNotIn("number_rooms", place.__dict__)
        self.assertIsInstance(Place.number_bathrooms, int)
        self.assertIn("number_bathrooms", dir(place))
        self.assertNotIn("number_bathrooms", place.__dict__)
        self.assertIsInstance(Place.max_guest, int)
        self.assertIn("max_guest", dir(place))
        self.assertNotIn("max_guest", place.__dict__)
        self.assertIsInstance(Place.price_by_night, int)
        self.assertIn("price_by_night", dir(place))
        self.assertNotIn("price_by_night", place.__dict__)
        self.assertIsInstance(Place.latitude, float)
        self.assertIn("latitude", dir(place))
        self.assertNotIn("latitude", place.__dict__)
        self.assertIsInstance(Place.longitude, float)
        self.assertIn("longitude", dir(place))
        self.assertNotIn("longitude", place.__dict__)
        self.assertIsInstance(Place.amenity_ids, list)
        self.assertIn("amenity_ids", dir(place))
        self.assertNotIn("amenity_ids", place.__dict__)

    def test_two_places_unique_ids(self):
        """Test that two places have unique IDs."""
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.id, place2.id)

    def test_two_places_different_created_at(self):
        """Test that two places have different 'created_at' timestamps."""
        place1 = Place()
        sleep(0.01)
        place2 = Place()
        self.assertLess(place1.created_at, place2.created_at)

    def test_two_places_different_updated_at(self):
        """Test that two places have different 'updated_at' timestamps."""
        place1 = Place()
        sleep(0.01)
        place2 = Place()
        self.assertLess(place1.updated_at, place2.updated_at)

    def test_str_representation(self):
        """Test the string representation of a Place object."""
        dt = datetime.today()
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = dt
        place_str = str(place)
        self.assertIn("[Place] (123456)", place_str)
        self.assertIn("'id': '123456'", place_str)
        self.assertIn(f"'created_at': {dt!r}", place_str)
        self.assertIn(f"'updated_at': {dt!r}", place_str)

    def test_args_unused(self):
        """Test instantiation with unused args."""
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation with keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        place = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place.id, "345")
        self.assertEqual(place.created_at, dt)
        self.assertEqual(place.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test instantiation with None keyword arguments."""
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlaceSave(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

    def test_save(self):
        """Test saving a Place instance."""
        place = Place()
        sleep(0.01)
        first_updated_at = place.updated_at
        place.save()
        self.assertLess(first_updated_at, place.updated_at)

    def test_save_updates_file(self):
        """Test that saving a Place instance updates the file."""
        place = Place()
        place.save()
        place_id = "Place." + place.id
        with open("file.json", "r") as file:
            self.assertIn(place_id, file.read())


class TestPlaceToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertIsInstance(Place().to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        place = Place()
        self.assertIn("id", place.to_dict())
        self.assertIn("created_at", place.to_dict())
        self.assertIn("updated_at", place.to_dict())
        self.assertIn("__class__", place.to_dict())

    def test_to_dict_contains_added_attributes(self):
        place = Place()
        place.middle_name = "ALXSE"
        place.my_number = 98
        self.assertEqual("ALXSE", place.middle_name)
        self.assertIn("my_number", place.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        place = Place()
        place_dict = place.to_dict()
        self.assertIsInstance(place_dict["id"], str)
        self.assertIsInstance(place_dict["created_at"], str)
        self.assertIsInstance(place_dict["updated_at"], str)

    def test_to_dict_output(self):
        dt = datetime.today()
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(place.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.to_dict(None)


if __name__ == "__main__":
    unittest.main()
