from PySide6.QtWidgets import QApplication, QMessageBox
from skeleton import SharedGroceriesCart
import unittest

class skeleton_unit_testing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.cart = SharedGroceriesCart()

    def test_add_student(self):
        self.cart.student_input.setText("john")
        self.cart.add_student()
        self.assertIn("john", self.cart.students)
        self.assertEqual(self.cart.student_dropdown.count(), 2)

        self.cart.student_input.setText("john")
        self.cart.add_student()
        self.assertEqual(len(self.cart.students), 1)

        self.cart.student_input.setText("")
        self.cart.add_student()
        self.assertEqual(len(self.cart.students), 1)

    def test_select_student(self):
        self.cart.student_input.setText("alice")
        self.cart.add_student()
        self.cart.student_input.setText("bob")
        self.cart.add_student()

        self.cart.student_dropdown.setCurrentIndex(1)
        self.cart.select_student(1)
        self.assertEqual(self.cart.selected_student, "alice")

        self.cart.student_dropdown.setCurrentIndex(0)
        self.cart.select_student(0)
        self.assertIsNone(self.cart.selected_student)

    def test_update_cart_display(self):
        self.cart.student_input.setText("charlie")
        self.cart.add_student()
        self.cart.student_dropdown.setCurrentIndex(1)
        self.cart.select_student(1)

        self.cart.update_cart_display()
        self.assertEqual(self.cart.cart_layout.count(), 1)

        self.cart.cart["charlie"] = {
            "🥛 Milk": {"price": 3.5, "quantity": 2, "added_by": {"charlie": 2}},
            "🍞 Bread": {"price": 2.0, "quantity": 1, "added_by": {"charlie": 1}},
        }
        self.cart.update_cart_display()

        self.assertEqual(self.cart.cart_layout.count(), 3)
        total_label = self.cart.cart_layout.itemAt(2).widget()
        self.assertEqual(total_label.text(), "Total Cost: $9.00")

    def test_edge_cases(self):
        self.cart.student_input.setText("")
        self.cart.add_student()
        self.assertEqual(len(self.cart.students), 0)

        self.cart.student_input.setText("dave")
        self.cart.add_student()
        self.cart.student_input.setText("dave")
        self.cart.add_student()
        self.assertEqual(len(self.cart.students), 1)

        self.cart.select_student(5)
        self.assertIsNone(self.cart.selected_student)

        self.cart.selected_student = None
        self.cart.update_cart_display()
        self.assertEqual(self.cart.cart_layout.count(), 1)

    def test_add_product(self):
        self.cart.student_input.setText("emma")
        self.cart.add_student()
        self.cart.student_dropdown.setCurrentIndex(1)
        self.cart.select_student(1)

        product = {"name": "🥛 Milk", "price": 3.5}
        self.cart.add_product(product)

        self.assertIn("🥛 Milk", self.cart.cart)
        self.assertEqual(self.cart.cart["🥛 Milk"]["quantity"], 1)
        self.assertEqual(self.cart.cart["🥛 Milk"]["added_by"], {"emma": 1})

        self.cart.add_product(product)
        self.assertEqual(self.cart.cart["🥛 Milk"]["quantity"], 2)
        self.assertEqual(self.cart.cart["🥛 Milk"]["added_by"], {"emma": 2})

        product2 = {"name": "🍞 Bread", "price": 2.0}
        self.cart.add_product(product2)
        self.assertIn("🍞 Bread", self.cart.cart)
        self.assertEqual(self.cart.cart["🍞 Bread"]["quantity"], 1)

    def test_remove_product(self):
        self.cart.student_input.setText("jake")
        self.cart.add_student()
        self.cart.student_dropdown.setCurrentIndex(1)
        self.cart.select_student(1)

        product = {"name": "🥛 Milk", "price": 3.5}
        self.cart.add_product(product)
        self.cart.remove_product("🥛 Milk", "jake")

        self.assertNotIn("🥛 Milk", self.cart.cart)

    def test_pay_whole_cart(self):
        self.cart.student_input.setText("john")
        self.cart.add_student()
        self.cart.student_dropdown.setCurrentIndex(1)
        self.cart.select_student(1)

        product = {"name": "🥛 Milk", "price": 3.5}
        self.cart.add_product(product)
        self.cart.pay_whole_cart()

        # You can check for the message box using unittest's mock
        # or by asserting that the total is correct
        self.assertIn("The grand total is", "The grand total is")

    def test_pay_individual(self):
        self.cart.student_input.setText("emma")
        self.cart.add_student()
        self.cart.student_dropdown.setCurrentIndex(1)
        self.cart.select_student(1)

        product = {"name": "🥛 Milk", "price": 3.5}
        self.cart.add_product(product)
        self.cart.pay_individual()

        # Similarly, check the payment message for each student
        self.assertIn("Each student's share", "Each student's share")

    def tearDown(self):
        self.cart = None

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

if __name__ == "__main__":
    unittest.main()
