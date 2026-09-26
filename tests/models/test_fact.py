import unittest
from uuid import UUID
from datetime import datetime, UTC
from models.source import *
from models.fact import *

class TestFactModel(unittest.TestCase):
    def test_create_fact(self):
        fh1 = Fact("Test Fact 1", ConfidenceType.HIGH, None)

        self.assertIsNotNone(fh1)
        self.assertIsNotNone(fh1.get_id())
        self.assertIsInstance(fh1.get_id(), UUID)
        self.assertEqual(fh1.confidence, ConfidenceType.HIGH)

    def test_ne(self):
        fh1 = Fact("Test Fact High", ConfidenceType.HIGH, None)
        fl1 = Fact("Test Fact Low", ConfidenceType.LOW, None)
        self.assertNotEqual(fh1, fl1)

    def test_add_source(self):
        fh1 = Fact("Test Fact High", ConfidenceType.HIGH, None)
        os1 = Source("Fact Test Source 1", "www.test.com", SourceType.OFFICIAL, "This is official fact")
        fh1.add_source(os1)
        self.assertEqual(len(fh1.sources), 1)

    def test_remove_source(self):
        fh1 = Fact("Test Fact High", ConfidenceType.HIGH, None)
        os1 = Source("Fact Test Source 1", "www.test.com", SourceType.OFFICIAL, "This is official fact")
        fh1.add_source(os1)
        fh1.remove_source(os1)
        self.assertEqual(len(fh1.sources), 0)


if __name__ == "__main__":
    unittest.main()
