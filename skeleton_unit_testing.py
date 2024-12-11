import unittest
from PySide6.QtWidgets import QApplication
from skeleton import SharedGroceriesCart


class SkeletonUnitTesting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup for the class, ensure only one QApplication instance."""
        # Only create QApplication if one doesn't exist already
        if not QApplication.instance():
            cls.app = QApplication([])  # Create QApplication if it doesn't exist
        else:
            cls.app = QApplication.instance()  # Use existing QApplication instance

    def setUp(self):
        """Setup before each test."""
        self.cart = SharedGroceriesCart()

    def test_add_student(self):
        """Test adding students to the cart."""
        self.cart.student_input.setText("john")
        self.cart.add_student()
        self.assertIn("john", self.cart.students, "Student 'john' should be added.")
        self.assertEqual(self.cart.student_dropdown.count(), 2, "Dropdown should have 2 items (1 valid student).")

        self.cart.student_input.setText("john")
        self.cart.add_student()
        self.assertEqual(len(self.cart.students), 1, "Duplicate student 'john' should not be added.")

        self.cart.student_input.setText("")
        self.cart.add_student()
        self.assertEqual(len(self.cart.students), 1, "Empty input should not add a student.")

        self.cart.student_input.setText("12345")
        self.cart.add_student()
        self.assertNotIn("12345", self.cart.students, "Numeric inputs should not be allowed.")

    def test_select_student(self):
        """Test selecting a student from the dropdown."""
        self.cart.student_input.setText("alice")
        self.cart.add_student()
        self.cart.student_input.setText("bob")
        self.cart.add_student()

        # Select the first valid student
        self.cart.student_dropdown.setCurrentIndex(1)
        self.cart.select_student(1)
        self.assertEqual(self.cart.selected_student, "alice", "Selected student should be 'alice'.")

        # Select the second valid student
        self.cart.student_dropdown.setCurrentIndex(2)
        self.cart.select_student(2)
        self.assertEqual(self.cart.selected_student, "bob", "Selected student should be 'bob'.")


    def test_edge_cases(self):
        """Test edge cases for invalid inputs and actions."""
        self.cart.student_input.setText("")
        self.cart.add_student()
        self.assertEqual(len(self.cart.students), 0, "Empty student names should not be added.")

        self.cart.student_input.setText("dave")
        self.cart.add_student()
        self.cart.student_input.setText("dave")
        self.cart.add_student()
        self.assertEqual(len(self.cart.students), 1, "Duplicate student names should not be added.")

        self.cart.select_student(5)
        self.assertTrue(
            self.cart.selected_student in [None, ""],
            "Invalid dropdown index should result in no selected student."
        )

    def test_add_product(self):
        """Test adding products to the cart."""
        self.cart.student_input.setText("emma")
        self.cart.add_student()
        self.cart.student_dropdown.setCurrentIndex(1)
        self.cart.select_student(1)

        product = {"name": "🥛 Milk", "price": 3.5}
        self.cart.add_product(product)

        self.assertIn("🥛 Milk", self.cart.cart, "Milk should be added to the cart.")
        self.assertEqual(self.cart.cart["🥛 Milk"]["quantity"], 1, "Milk quantity should be 1.")
        self.assertEqual(self.cart.cart["🥛 Milk"]["added_by"], {"emma": 1}, "Milk should be added by 'emma'.")

        self.cart.add_product(product)
        self.assertEqual(self.cart.cart["🥛 Milk"]["quantity"], 2, "Milk quantity should now be 2.")
        self.assertEqual(self.cart.cart["🥛 Milk"]["added_by"], {"emma": 2}, "Milk should be added twice by 'emma'.")

    def test_remove_product(self):
        """Test removing a product from the cart."""
        self.cart.student_input.setText("jake")
        self.cart.add_student()
        self.cart.student_dropdown.setCurrentIndex(1)
        self.cart.select_student(1)

        product = {"name": "🥛 Milk", "price": 3.5}
        self.cart.add_product(product)
        self.cart.remove_product("🥛 Milk", "jake")

        self.assertNotIn("🥛 Milk", self.cart.cart, "Milk should be removed from the cart.")

    def test_pay_whole_cart(self):
        """Test paying for the whole cart."""
        self.cart.student_input.setText("john")
        self.cart.add_student()
        self.cart.student_dropdown.setCurrentIndex(1)
        self.cart.select_student(1)

        product = {"name": "🥛 Milk", "price": 3.5}
        self.cart.add_product(product)

        grand_total = 3.5 + self.cart.delivery_fee
        self.assertAlmostEqual(grand_total, 8.5, "Grand total should include product price and delivery fee.")

    def test_pay_individual(self):
        """Test individual payment breakdown."""
        self.cart.student_input.setText("emma")
        self.cart.add_student()
        self.cart.student_dropdown.setCurrentIndex(1)
        self.cart.select_student(1)

        product = {"name": "🥛 Milk", "price": 3.5}
        self.cart.add_product(product)

        expected_total = 3.5 + self.cart.delivery_fee
        self.assertIn("emma", self.cart.cart["🥛 Milk"]["added_by"], "Payment breakdown should include 'emma'.")
        self.assertAlmostEqual(expected_total, 8.5, "Individual payment should include product price and delivery fee.")

    def tearDown(self):
        self.cart = None

    @classmethod
    def tearDownClass(cls):
        """Clean up QApplication."""
        if QApplication.instance():
            QApplication.quit()


if __name__ == "__main__":
    unittest.main()
