import unittest
from PySide6.QtWidgets import QApplication
from skeleton import SharedGroceriesCart


class skeleton_unit_testing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # setting up the app for all tests
        cls.app = QApplication([])

    def setUp(self):
        # create a new cart instance before every test
        self.cart = SharedGroceriesCart()

    def test_add_student(self):
        # check if adding a student works

        # adding a normal student
        self.cart.student_input.setText("john")
        self.cart.add_student()
        self.assertIn("john", self.cart.students, "john should be in the students list")
        self.assertEqual(self.cart.student_dropdown.count(), 2, "dropdown should have 2 items (1 valid)")

        # try adding the same student again, shouldn't work
        self.cart.student_input.setText("john")
        self.cart.add_student()
        self.assertEqual(len(self.cart.students), 1, "duplicate students shouldn't be added")
        self.assertEqual(self.cart.student_dropdown.count(), 2, "dropdown count shouldn't increase")

        # adding an empty student name
        self.cart.student_input.setText("")
        self.cart.add_student()
        self.assertEqual(len(self.cart.students), 1, "empty names shouldn't be added to the students list")
        self.assertEqual(self.cart.student_dropdown.count(), 2, "dropdown count shouldn't change for empty input")

    def test_select_student(self):
        # test selecting a student from the dropdown

        # add a couple of students to select
        self.cart.student_input.setText("alice")
        self.cart.add_student()
        self.cart.student_input.setText("bob")
        self.cart.add_student()

        # select the first valid student
        self.cart.student_dropdown.setCurrentIndex(1)  # "alice"
        self.cart.select_student(1)
        self.assertEqual(self.cart.selected_student, "alice", "selected student should be alice")

        # reset to no selection
        self.cart.student_dropdown.setCurrentIndex(0)  # default option
        self.cart.select_student(0)
        self.assertIsNone(self.cart.selected_student, "selected student should be None if no valid choice is made")

    def test_update_cart_display(self):
        # make sure the cart UI updates properly

        # add a student and select them
        self.cart.student_input.setText("charlie")
        self.cart.add_student()
        self.cart.student_dropdown.setCurrentIndex(1)  # select "charlie"
        self.cart.select_student(1)

        # when the cart is empty, it should show an empty cart message
        self.cart.update_cart_display()
        self.assertEqual(self.cart.cart_layout.count(), 1, "cart should display a message if it's empty")

        # add some products to charlie's cart
        self.cart.cart["charlie"] = {
            "🥛 Milk": {"price": 3.5, "quantity": 2},
            "🍞 Bread": {"price": 2.0, "quantity": 1},
        }
        self.cart.update_cart_display()

        # check that the display has updated correctly
        self.assertEqual(self.cart.cart_layout.count(), 3, "cart should show 2 items and the total cost")
        total_label = self.cart.cart_layout.itemAt(2).widget()
        self.assertEqual(total_label.text(), "Total Cost: $9.00", "total cost should match the items in the cart")

    def test_edge_cases(self):
        # test empty inputs or duplicate entries

        # empty name
        self.cart.student_input.setText("")
        self.cart.add_student()
        self.assertEqual(len(self.cart.students), 0, "empty student names shouldn't be added")

        # duplicate student names
        self.cart.student_input.setText("dave")
        self.cart.add_student()
        self.cart.student_input.setText("dave")
        self.cart.add_student()
        self.assertEqual(len(self.cart.students), 1, "duplicate names shouldn't be added twice")

        # selecting a student that doesn't exist
        self.cart.select_student(5)  # invalid index
        self.assertIsNone(self.cart.selected_student, "should handle invalid dropdown indices gracefully")

        # updating cart with no selected student
        self.cart.selected_student = None
        self.cart.update_cart_display()
        self.assertEqual(self.cart.cart_layout.count(), 1, "cart should display a message when no student is selected")

    def test_add_product(self):
        # test adding items to a student's cart
        pass

    def test_remove_product(self):
        # check if removing items from the cart works
        pass

    def test_pay_whole_cart(self):
        # test the payment for the entire cart
        pass

    def test_pay_individual(self):
        # check the payment for just one person
        pass

    def tearDown(self):
        # close the cart after each test
        self.cart.close()

    @classmethod
    def tearDownClass(cls):
        # clean up the app after all tests are done
        cls.app.quit()


if __name__ == "__main__":
    unittest.main()
