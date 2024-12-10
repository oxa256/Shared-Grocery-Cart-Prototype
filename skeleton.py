from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt
import sys


class SharedGroceriesCart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSH Shared Groceries Cart")
        self.setGeometry(100, 100, 900, 700)

        # List to store student names
        self.students = []
        self.selected_student = None

        # Dictionary to store products in the cart
        self.cart = {}

        # List of products with name and price
        self.products = [
            {"name": "🥛 Milk", "price": 3.5},
            {"name": "🍞 Bread", "price": 2.0},
            {"name": "🥚 Eggs", "price": 2.5},
            {"name": "🧀 Cheese", "price": 4.0},
        ]
        self.delivery_fee = 5.0  # Fixed delivery fee

        self.initUI()

    def initUI(self):
        """Set up the user interface components."""
        # This function sets up the layout, widgets, and buttons.
        # Use a combination of QVBoxLayout and QHBoxLayout to arrange the UI components.
        # Add labels, buttons, input fields, and other necessary widgets.

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("-SSH Shared Groceries Cart-", alignment=Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #5DADE2; margin-bottom: 20px;")
        main_layout.addWidget(title)



         # Payment and Reset Buttons
        payment_layout = QHBoxLayout()

        pay_whole_btn = QPushButton("Pay for Everyone 💳")
        pay_whole_btn.setStyleSheet("background-color: #5DADE2; color: white; padding: 10px; border-radius: 5px;")
        pay_whole_btn.clicked.connect(self.pay_whole_cart)

        pay_individual_btn = QPushButton("Pay Individually 🧾")
        pay_individual_btn.setStyleSheet("background-color: #85C1E9; color: white; padding: 10px; border-radius: 5px;")
        pay_individual_btn.clicked.connect(self.pay_individual)

    


        reset_cart_btn = QPushButton("Resert Cart 🔄")
        reset_cart_btn.setStyleSheet("background-color: #E74C3C; color: white; padding: 10px; border-radius: 5px;")
        reset_cart_btn.clicked.connect(self.reset_cart)


        payment_layout.addWidget(pay_whole_btn)
        payment_layout.addWidget(pay_individual_btn)
        payment_layout.addWidget(reset_cart_btn)


        main_layout.addLayout(payment_layout)

        # Add Student Section
        student_layout = QVBoxLayout()
        student_layout.addWidget(QLabel("Add a student:", alignment=Qt.AlignLeft))
        self.student_input = QLineEdit()
        self.student_input.setPlaceholderText("Enter student name")
        student_layout.addWidget(self.student_input)

        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)
        student_layout.addWidget(add_student_button)

        # Student Dropdown
        self.student_dropdown = QComboBox()
        self.student_dropdown.addItem("-- Select Student --")
        self.student_dropdown.currentIndexChanged.connect(self.select_student)
        student_layout.addWidget(self.student_dropdown)

        main_layout.addLayout(student_layout)

        # Cart Display Section
        self.cart_display = QScrollArea()
        self.cart_widget = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_widget)
        self.cart_display.setWidget(self.cart_widget)
        self.cart_display.setWidgetResizable(True)
        self.cart_display.setStyleSheet("background-color: #ECF0F1; border: 1px solid #D5D8DC;")
        main_layout.addWidget(self.cart_display)

    def add_student(self):
        """Add a new student to the cart."""
        student_name = self.student_input.text().strip()
        if not student_name:
            QMessageBox.warning(self, "Error", "Student name cannot be empty!")
            return

        if student_name in self.students:
            QMessageBox.warning(self, "Error", f"Student '{student_name}' already exists!")
            return

        # Add student and clear input
        self.students.append(student_name)
        self.cart[student_name] = {}  # Initialize their cart
        self.student_dropdown.addItem(student_name)
        self.student_input.clear()
        QMessageBox.information(self, "Success", f"Student '{student_name}' added successfully!")

    def select_student(self, index):
        """Update the selected student based on the dropdown selection."""
        if index <= 0:
            self.selected_student = None
            QMessageBox.warning(self, "Error", "Please select a valid student!")
            return

        # Update the selected student
        self.selected_student = self.student_dropdown.itemText(index)
        QMessageBox.information(self, "Selection Updated", f"'{self.selected_student}' is now selected.")

    def update_cart_display(self):
        """Update the cart display with the current state of the cart."""
        # Clear existing cart items
        while self.cart_layout.count():
            child = self.cart_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self.selected_student:
            empty_label = QLabel("No student selected. Select a student to see their cart.")
            empty_label.setStyleSheet("color: gray; font-style: italic; margin: 10px;")
            self.cart_layout.addWidget(empty_label)
            return

        # Display the selected student's cart
        student_cart = self.cart.get(self.selected_student, {})
        if not student_cart:
            empty_label = QLabel(f"{self.selected_student} has no items in their cart.")
            empty_label.setStyleSheet("color: gray; font-style: italic; margin: 10px;")
            self.cart_layout.addWidget(empty_label)
            return

        total_cost = 0
        for product_name, details in student_cart.items():
            quantity = details["quantity"]
            price = details["price"]
            total_cost += quantity * price

            # Product display
            product_label = QLabel(f"{product_name} x{quantity} - ${quantity * price:.2f}")
            product_label.setStyleSheet("margin-bottom: 10px; padding: 5px; background-color: #ECF0F1; border-radius: 4px;")
            self.cart_layout.addWidget(product_label)

        # Display the total cost
        total_label = QLabel(f"Total Cost: ${total_cost:.2f}")
        total_label.setStyleSheet("font-weight: bold; color: #2ECC71; margin-top: 15px;")
        self.cart_layout.addWidget(total_label)

    def add_product(self, product):
        """Add a selected product to the current student's cart."""
        # This function should add the product to the selected student's cart.
        # If the product already exists in the cart, increase the quantity.
        # Otherwise, add it as a new item. omar made a change eher 
        

    def remove_product(self, product_name):
        """Remove a product from the cart for the selected student."""
        # This function should handle removing a product from the cart.
        # Check if the selected student has added that product before removing it.

    def pay_whole_cart(self):
        """Calculate and display the total cost for everyone."""
        # This function should calculate the grand total for all students' products
        # and include the delivery fee. Display the total using QMessageBox.

    def pay_individual(self):
        """Calculate and display the total cost per student."""
        # This function should calculate the total amount each student owes based on their contributions.
        # Display the breakdown of payments using QMessageBox.

    def reset_cart(self):
        """Reset the cart to its initial state."""
    self.cart = {}
    self.selected_student = None
    self.student_dropdown.setCurrentIndex(0)
    self.update_cart_display()

    QMessageBox.information(self, "Cart reset")




# Main execution
def main():
    app = QApplication(sys.argv)
    window = SharedGroceriesCart()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
