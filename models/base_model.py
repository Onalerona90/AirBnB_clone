#!/usr/bin/python3
"""This script is the base model"""
import uuid
import datetime
from models import storage


class BaseModel:
    def __init__(self, *args, **kwargs):
        """
        Constructor for the BaseModel class.

        Args:
            *args: Non-keyword arguments (not used in this implementation).
            **kwargs: Keyword arguments for initializing instance attributes.
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            storage.new(self)
        else:
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    setattr(
                        self, key, datetime.datetime.strptime(
                            value, date_format))
                elif key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.
        """
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates the 'updated_at' attribute to
        the current timestamp and saves the instance.
        """
        self.updated_at = datetime.datetime.now()
        storage.save()

    def to_dict(self):
        """
        Converts the instance to a dictionary for serialization.
        """
        object_dict = {
            key: value for key,
            value in self.__dict__.items() if key not in [
                "created_at", "updated_at"
            ]
        }
        object_dict.update({
            "__class__": self.__class__.__name__,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        })
        return object_dict
