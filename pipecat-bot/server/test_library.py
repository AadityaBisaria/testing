import unittest

from library import LibraryCatalog


class LibraryCatalogTests(unittest.TestCase):
    def setUp(self):
        self.catalog = LibraryCatalog()

    def test_can_search_rent_and_receive_a_book(self):
        matches = self.catalog.search("hobbit")
        self.assertEqual(matches[0]["title"], "The Hobbit")
        self.assertTrue(matches[0]["available"])

        rental = self.catalog.rent("The Hobbit", "Aaditya")
        self.assertTrue(rental["success"])
        self.assertEqual(self.catalog.loans_for("aaditya")[0]["title"], "The Hobbit")

        receipt = self.catalog.receive("The Hobbit")
        self.assertTrue(receipt["success"])
        self.assertEqual(self.catalog.loans_for("Aaditya"), [])

    def test_cannot_rent_an_already_checked_out_book(self):
        self.catalog.rent("Dune", "Aaditya")
        result = self.catalog.rent("Dune", "Mira")
        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
