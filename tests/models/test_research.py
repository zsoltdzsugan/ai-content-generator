import unittest
from uuid import UUID
from datetime import datetime, UTC
from models.research import *
from models.source import *
from models.fact import *

class TestResearchModel(unittest.TestCase):
    def test_create_research(self):
        tr1 = Research("Test Research 1")

        self.assertIsNotNone(tr1)
        self.assertIsNotNone(tr1.get_id())
        self.assertIsInstance(tr1.get_id(), UUID)
        self.assertEqual(tr1.status, ResearchStatus.CREATED)
        self.assertIsInstance(tr1.created_at, datetime)

    def test_eq(self):
        tr1 = Research("Test Research 1")
        tr2 = tr1
        tr2.status = ResearchStatus.COMPLETED
        os1 = Source("Test Source 1", "www.test.com", SourceType.OFFICIAL, "This is official content")
        tr2.add_source(os1)
        self.assertEqual(tr1, tr2)

    def test_ne(self):
        tr1 = Research("Test Research 1")
        tr2 = Research("Test Research 2")
        self.assertNotEqual(tr1, tr2)

    def test_add_source(self):
        tr1 = Research("Test Research 1")
        os1 = Source("Test Source 1", "www.test.com", SourceType.OFFICIAL, "This is official content")
        tr1.add_source(os1)
        self.assertEqual(len(tr1.sources), 1)

    def test_remove_source(self):
        tr1 = Research("Test Research 1")
        os1 = Source("Test Source 1", "www.test.com", SourceType.OFFICIAL, "This is official content")
        tr1.add_source(os1)
        tr1.remove_source(os1)
        self.assertEqual(len(tr1.sources), 0)

    def test_add_fact(self):
        tr1 = Research("Test Research 1")
        fh1 = Fact("Test Fact 1", ConfidenceType.HIGH, None)
        tr1.add_fact(fh1)
        self.assertEqual(len(tr1.facts), 1)

    def test_remove_fact(self):
        tr1 = Research("Test Research 1")
        fh1 = Fact("Test Fact 1", ConfidenceType.HIGH, None)
        tr1.add_fact(fh1)
        tr1.remove_fact(fh1)
        self.assertEqual(len(tr1.facts), 0)

if __name__ == "__main__":
    unittest.main()
