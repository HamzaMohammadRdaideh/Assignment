import unittest
from unittest.mock import MagicMock

from fastapi.encoders import jsonable_encoder

from app.api.v1.depandancies.hash import Hasher
from app.api.v1.repositories.user import list_users, create_user
from core.database.connection import db
from core.exceptions.user import UserCreateError


class TestUserFunctions(unittest.TestCase):

    def setUp(self):
        # Mock db.client if it's None
        if db.client is None:
            db.client = MagicMock()

        # Mock db.client["user"] if it's None
        if db.client.get("user") is None:
            db.client["user"] = MagicMock()

        # Now safely assign the user_collection mock
        self.user_collection = MagicMock()
        db.client["user"].users = self.user_collection

    def tearDown(self):
        db.client["user"].users = None

    def test_list_users(self):
        # Mock the data returned from the user collection
        mock_data = [
            {"_id": "1", "name": "John Doe"},
            {"_id": "2", "name": "Jane Smith"}
        ]
        self.user_collection.find.return_value = mock_data

        # Call the function
        response = list_users()

        # Assert the response
        expected_response = jsonable_encoder(mock_data)
        self.assertEqual(response, expected_response)