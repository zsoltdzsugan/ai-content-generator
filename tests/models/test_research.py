import unittest
from uuid import UUID
from datetime import datetime, UTC
from models.research import *

class TestTextNode(unittest.TestCase):
    def test_create_research(self):
        tr1 = Research("Test Research 1")

        self.assertIsNotNone(tr1)
        self.assertIsNotNone(tr1.get_id())
        self.assertIsInstance(tr1.get_id(), UUID)
        self.assertEqual(tr1.status, ResearchStatus.CREATED)
        self.assertIsInstance(tr1.created_at, datetime)

    def test_ne(self):
        tr1 = Research("Test Research 1")
        tr2 = Research("Test Research 2")
        self.assertNotEqual(tr1, tr2)


if __name__ == "__main__":
    unittest.main()
