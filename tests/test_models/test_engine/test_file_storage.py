#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.
Unittest classes:
    TestFileStorageInstantiation
    TestFileStorageMethods
"""

import os
import models
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestFileStorageInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up the class for testing."""
        cls.tmp_file = "tmp"
        try:
            os.rename(FileStorage._FileStorage__file_path, cls.tmp_file)
        except FileNotFoundError:
            pass

    @classmethod
    def tearDownClass(cls):
        """Clean up after testing."""
        try:
            os.remove(FileStorage._FileStorage__file_path)
        except FileNotFoundError:
            pass
        try:
            os.rename(cls.tmp_file, FileStorage._FileStorage__file_path)
        except FileNotFoundError:
            pass

    def test_instantiation_no_args(self):
        """Test FileStorage instantiation with no arguments."""
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_instantiation_with_arg(self):
        """Test FileStorage instantiation with an argument."""
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_file_path_is_private_str(self):
        """Test that __file_path is a private string attribute."""
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_objects_is_private_dict(self):
        """Test that __objects is a private dictionary attribute."""
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        """Test that models.storage is an instance of FileStorage."""
        self.assertIsInstance(models.storage, FileStorage)


class TestFileStorageMethods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up for testing."""
        cls.tmp_file = "tmp"
        try:
            os.rename(FileStorage._FileStorage__file_path, cls.tmp_file)
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        """Clean up after testing."""
        try:
            os.remove(FileStorage._FileStorage__file_path)
        except IOError:
            pass
        try:
            os.rename(cls.tmp_file, FileStorage._FileStorage__file_path)
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        """Test the all() method of FileStorage."""
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        """Test the all() method of FileStorage with an argument."""
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        """Test the new() method of FileStorage."""
        models_to_test = [
            BaseModel(),
            User(),
            State(),
            Place(),
            City(),
            Amenity(),
            Review()
        ]
        for model in models_to_test:
            models.storage.new(model)
            self.assertIn(
                f"{model.__class__.__name__}.{model.id}", models.storage.all())
            self.assertIn(model, models.storage.all().values())

    def test_new_with_args(self):
        """Test the new() method with arguments."""
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_with_None(self):
        """Test the new() method with None."""
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save(self):
        """Test the save() method of FileStorage."""
        models_to_test = [
            BaseModel(),
            User(),
            State(),
            Place(),
            City(),
            Amenity(),
            Review()
        ]
        for model in models_to_test:
            models.storage.new(model)
        models.storage.save()
        with open(FileStorage._FileStorage__file_path, "r") as f:
            save_text = f.read()
            for model in models_to_test:
                self.assertIn(
                    f"{model.__class__.__name__}.{model.id}", save_text)

    def test_save_with_arg(self):
        """Test the save() method with an argument."""
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        """Test the reload() method of FileStorage."""
        models_to_test = [
            BaseModel(),
            User(),
            State(),
            Place(),
            City(),
            Amenity(),
            Review()
        ]
        for model in models_to_test:
            models.storage.new(model)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        for model in models_to_test:
            self.assertIn(f"{model.__class__.__name__}.{model.id}", objs)

    def test_reload_with_arg(self):
        """Test the reload() method with an argument."""
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
