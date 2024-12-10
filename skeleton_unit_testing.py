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
        pass

    def test_select_student(self):
        # test selecting a student from the dropdown
        pass

    def test_add_product(self):
        # test adding items to a student's cart
        pass

    def test_remove_product(self):
        # check if removing items from the cart works
        pass

    def test_update_cart_display(self):
        # make sure the cart UI updates properly
        pass

    def test_pay_whole_cart(self):
        # test the payment for the entire cart
        pass

    def test_pay_individual(self):
        # check the payment for just one person
        pass

    def test_edge_cases(self):
        # test weird stuff like empty inputs or duplicate entries
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
