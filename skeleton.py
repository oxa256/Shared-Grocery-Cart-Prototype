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

        self.init_ui()

    def init_ui(self):
        """Set up the user interface components."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("-SSH Shared Groceries Cart-", alignment=Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #5DADE2; margin-bottom:20px;")
        main_layout.addWidget(title)

        # Add Student Section
        student_layout = QVBoxLayout()
        student_layout.addWidget(QLabel("Add a student:", 
                                        alignment=Qt.AlignLeft))
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

        # Product Selection Section
        product_layout = QHBoxLayout()
        product_label = QLabel("Available Products:", alignment=Qt.AlignLeft)
        product_layout.addWidget(product_label)

        # Add product buttons
        for product in self.products:
            product_button = QPushButton(
                f"{product['name']} - ${product['price']:.2f}"
            )
            product_button.setStyleSheet(
                "background-color: #D5E8FB; padding: 5px 10px; border-radius: 5px;"
            )
            product_button.clicked.connect(lambda _, p=product: self.add_product(p))
            product_layout.addWidget(product_button)

        main_layout.addLayout(product_layout)

        # Cart Display Section
        self.cart_display = QScrollArea()
        self.cart_widget = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_widget)
        self.cart_display.setWidget(self.cart_widget)
        self.cart_display.setWidgetResizable(True)
        self.cart_display.setStyleSheet(
            "background-color: #ECF0F1; border: 1px solid #D5D8DC;"
        )
        main_layout.addWidget(self.cart_display)

        # Payment and Reset Buttons
        payment_layout = QHBoxLayout()
        payment_layout.setSpacing(10)
        payment_layout.setContentsMargins(0, 20, 0, 0)

        pay_whole_btn = QPushButton("Pay for Everyone 💳")
        pay_whole_btn.setStyleSheet(
            "background-color: #5DADE2; color: white; padding: 10px; border-radius: 5px;"
        )
        pay_whole_btn.clicked.connect(self.pay_whole_cart)
        pay_whole_btn.setFixedHeight(40)

        pay_individual_btn = QPushButton("Pay Individually 🧾")
        pay_individual_btn.setStyleSheet(
            "background-color: #5DADE2; color: white; padding: 10px; border-radius: 5px;"
        )
        pay_individual_btn.clicked.connect(self.pay_individual)
        pay_individual_btn.setFixedHeight(40)

        reset_cart_btn = QPushButton("Reset Cart 🔄")
        reset_cart_btn.setStyleSheet(
            "background-color: #E74C3C; color: white; padding: 10px; border-radius: 5px;"
        )
        reset_cart_btn.clicked.connect(self.reset_cart)
        reset_cart_btn.setFixedHeight(40)

        payment_layout.addWidget(pay_whole_btn)
        payment_layout.addWidget(pay_individual_btn)
        payment_layout.addWidget(reset_cart_btn)
        payment_layout.addStretch()

        main_layout.addLayout(payment_layout)

    def add_student(self):
        """Add a new student to the cart."""
        student_name = self.student_input.text().strip()
        if not student_name.isalpha() and not all(
            c.isalpha() or c.isspace() for c in student_name
        ):
            QMessageBox.warning(
                self, "Invalid Input", "Student name must contain only letters and spaces!"
            )
            return

        if not student_name:
            QMessageBox.warning(self, "Error", "Student name cannot be empty!")
            return

        if student_name in self.students:
            QMessageBox.warning(
                self, "Error", f"Student '{student_name}' already exists!"
            )
            return

        self.students.append(student_name)
        self.student_dropdown.addItem(student_name)
        self.student_input.clear()
        QMessageBox.information(
            self, "Success", f"Student '{student_name}' added successfully!"
        )

    def select_student(self, index):
        """Update the selected student based on the dropdown selection."""
        if index <= 0:
            self.selected_student = None
            QMessageBox.warning(self, "Error", "Please select a valid student!")
            return

        self.selected_student = self.student_dropdown.itemText(index)
        QMessageBox.information(
            self, "Selection Updated", f"'{self.selected_student}' is now selected."
        )

    def update_cart_display(self):
        """Update the cart display with current cart data."""
        while self.cart_layout.count():
            child = self.cart_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self.cart:
            empty_label = QLabel("The cart is empty. Add items to see them here.")
            empty_label.setStyleSheet("color: gray; font-style: italic; margin: 10px;")
            self.cart_layout.addWidget(empty_label)
            return

        for product_name, product_data in self.cart.items():
            product_header = QLabel(f"{product_name} - ${product_data['price']:.2f}")
            product_header.setStyleSheet("font-weight: bold; margin-top: 10px;")
            self.cart_layout.addWidget(product_header)

            for student, quantity in product_data["added_by"].items():
                subtotal = product_data["price"] * quantity
                student_info = QLabel(
                    f"{student}: {quantity} x ${product_data['price']:.2f} = ${subtotal:.2f}"
                )
                student_info.setStyleSheet("margin-left: 15px;")
                self.cart_layout.addWidget(student_info)

    def add_product(self, product):
        """Add a product to the cart."""
        if self.selected_student is None:
            QMessageBox.warning(self, "Error", "Please select a student first!")
            return

        if product["name"] not in self.cart:
            self.cart[product["name"]] = {
                "price": product["price"],
                "quantity": 1,
                "added_by": {self.selected_student: 1},
            }
        else:
            self.cart[product["name"]]["quantity"] += 1
            self.cart[product["name"]]["added_by"][self.selected_student] = (
                self.cart[product["name"]]["added_by"].get(self.selected_student, 0) + 1
            )
        self.update_cart_display()

    def remove_product(self, product_name, student_name):
        """Remove a product from a student's cart."""
        if product_name in self.cart and student_name in self.cart[product_name]["added_by"]:
            del self.cart[product_name]["added_by"][student_name]
            if not self.cart[product_name]["added_by"]:
                del self.cart[product_name]
            self.update_cart_display()

    def pay_whole_cart(self):
        """Calculate total cost of the cart."""
        if not self.cart:
            QMessageBox.warning(self, "Oops!", "The cart is empty!")
            return

        grand_total = sum(
            product["price"] * product["quantity"] for product in self.cart.values()
        ) + self.delivery_fee
        QMessageBox.information(self, "Payment", f"Grand total: ${grand_total:.2f}")

    def pay_individual(self):
        """Calculate individual payment breakdown."""
        if not self.cart:
            QMessageBox.warning(self, "Oops!", "The cart is empty!")
            return

        payments = {student: 0 for student in self.students}
        for product_name, product_data in self.cart.items():
            for student, quantity in product_data["added_by"].items():
                payments[student] += product_data["price"] * quantity

        contributing_students = [s for s, total in payments.items() if total > 0]
        if contributing_students:
            delivery_fee_per_student = self.delivery_fee / len(contributing_students)
            for student in contributing_students:
                payments[student] += delivery_fee_per_student

        payment_info = "\n".join(
            [f"{student}: ${total:.2f}" for student, total in payments.items() if total > 0]
        )
        QMessageBox.information(self, "Payment Breakdown", f"Each student's share:\n{payment_info}")

    def reset_cart(self):
        """Reset the cart and UI."""
        self.cart.clear()
        self.update_cart_display()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SharedGroceriesCart()
    window.show()
    sys.exit(app.exec())
