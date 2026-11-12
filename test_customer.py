import unittest
from customer import (validate_code, validate_name, validate_birth_date,
                      CustomerDB, fits_screen)

class TestCustomer(unittest.TestCase):
    # R1 - personal code
    def test_TC001_valid_code(self):
        self.assertTrue(validate_code("47503020193"))
    def test_TC002_code_too_short(self):
        self.assertFalse(validate_code("4750302019"))
    def test_TC003_code_with_letters(self):
        self.assertFalse(validate_code("4750302019A"))
    def test_TC004_code_wrong_checksum(self):
        self.assertFalse(validate_code("47503020194"))
    # R2 - names
    def test_TC005_lithuanian_letters_accepted(self):
        self.assertTrue(validate_name("Onutė") and validate_name("Onaitytė"))
    def test_TC006_digits_in_name_rejected(self):
        self.assertFalse(validate_name("Onut3"))
    # R3 - date of birth
    def test_TC007_valid_date(self):
        self.assertTrue(validate_birth_date("02.03.1975"))
    def test_TC008_year_only_rejected(self):
        self.assertFalse(validate_birth_date("1975"))
    # R4 - saving
    def test_TC009_valid_customer_saved(self):
        db = CustomerDB()
        db.add("47503020193", "Onutė", "Onaitytė", "02.03.1975")
        self.assertEqual(db.get("47503020193"), ("Onutė", "Onaitytė", "02.03.1975"))
    def test_TC010_invalid_customer_not_saved(self):
        db = CustomerDB()
        with self.assertRaises(ValueError):
            db.add("47503020193", "Onutė", "Onaitytė", "1975")
        self.assertEqual(db.count(), 0)
    # R5 - duplicates
    def test_TC011_duplicate_code_rejected(self):
        db = CustomerDB()
        db.add("47503020193", "Onutė", "Onaitytė", "02.03.1975")
        with self.assertRaises(KeyError):
            db.add("47503020193", "Jonas", "Jonaitis", "01.01.1980")
        self.assertEqual(db.count(), 1)
    # R6 - screen size
    def test_TC012_window_fits_800x600(self):
        self.assertTrue(fits_screen(800, 600))
        self.assertFalse(fits_screen(801, 600))

if __name__ == "__main__":
    unittest.main()
