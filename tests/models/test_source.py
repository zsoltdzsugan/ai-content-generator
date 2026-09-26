import unittest
from uuid import UUID
from datetime import datetime, UTC
from models.source import *


class TestSourceModel(unittest.TestCase):
    def test_create_source(self):
        os1 = Source("Test Source 1", "www.test.com", SourceType.OFFICIAL, "This is official content")

        self.assertIsNotNone(os1)
        self.assertIsNotNone(os1.get_id())
        self.assertIsInstance(os1.get_id(), UUID)
        self.assertEqual(os1.type, SourceType.OFFICIAL)
        self.assertIsInstance(os1.created_at, datetime)

    def test_ne(self):
        os1 = Source("Test Source 1", "www.test.com", SourceType.OFFICIAL, "This is official content")
        ws1 = Source("Test Source 2", "www.test2.com", SourceType.WIKI, "This is wiki content")
        self.assertNotEqual(os1, ws1)


if __name__ == "__main__":
    unittest.main()
