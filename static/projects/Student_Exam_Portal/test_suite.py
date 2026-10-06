"""
Automated Test Suite for Student Exam Portal
Engineered autonomously by J.A.R.V.I.S. Tester Agent.
100% deterministic unit tests for database and business logic.
"""

import unittest
import os
import database


class TestStudentExamPortal(unittest.TestCase):

    def setUp(self):
        database.init_db()

    def test_add_and_retrieve_item(self):
        new_id = database.add_item("Unit Test Task Item", "testing")
        self.assertIsNotNone(new_id)
        self.assertGreater(new_id, 0)

        retrieved = database.get_item_by_id(new_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["title"], "Unit Test Task Item")
        self.assertEqual(retrieved["category"], "testing")

    def test_get_items_filtered(self):
        database.add_item("Alpha Task", "alpha_cat")
        items = database.get_items(category="alpha_cat")
        self.assertTrue(len(items) >= 1)
        self.assertTrue(all(it["category"] == "alpha_cat" for it in items))

    def test_delete_item(self):
        del_id = database.add_item("To Be Deleted", "temp")
        success = database.delete_item(del_id)
        self.assertTrue(success)
        self.assertIsNone(database.get_item_by_id(del_id))

    def test_hash_credential_security(self):
        h1 = database.hash_credential("supersecret")
        h2 = database.hash_credential("supersecret")
        self.assertEqual(h1, h2)
        self.assertNotEqual(h1, "supersecret")


if __name__ == "__main__":
    unittest.main()
