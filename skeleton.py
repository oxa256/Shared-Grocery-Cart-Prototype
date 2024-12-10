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

        # Product Selection Section (new)
        product_layout = QHBoxLayout()
        product_label = QLabel("Available Products:", alignment=Qt.AlignLeft)
        product_layout.addWidget(product_label)
        
        # Add product buttons
        for product in self.products:
            product_button = QPushButton(f"{product['name']} - ${product['price']:.2f}")
            product_button.setStyleSheet("background-color: #D5E8FB; padding: 5px 10px; border-radius: 5px;")
            product_button.clicked.connect(lambda _, p=product: self.add_product(p))
            product_layout.addWidget(product_button)
        
        main_layout.addLayout(product_layout)


        # Cart Display Section
        self.cart_display = QScrollArea()
        self.cart_widget = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_widget)
        self.cart_display.setWidget(self.cart_widget)
        self.cart_display.setWidgetResizable(True)
        self.cart_display.setStyleSheet("background-color: #ECF0F1; border: 1px solid #D5D8DC;")
        main_layout.addWidget(self.cart_display)

        # Payment and Reset Buttons
        payment_layout = QHBoxLayout()
        payment_layout.setSpacing(10)  # Ensuring enough space between buttons
        payment_layout.setContentsMargins(0, 20, 0, 0)  # Add space above the buttons

        pay_whole_btn = QPushButton("Pay for Everyone 💳")
        pay_whole_btn.setStyleSheet("background-color: #5DADE2; color: white; padding: 10px; border-radius: 5px;")
        pay_whole_btn.clicked.connect(self.pay_whole_cart)
        pay_whole_btn.setFixedHeight(40)

        pay_individual_btn = QPushButton("Pay Individually 🧾")
        pay_individual_btn.setStyleSheet("background-color: #5DADE2; color: white; padding: 10px; border-radius: 5px;")
        pay_individual_btn.clicked.connect(self.pay_individual)
        pay_individual_btn.setFixedHeight(40)

        reset_cart_btn = QPushButton("Reset Cart 🔄")
        reset_cart_btn.setStyleSheet("background-color: #E74C3C; color: white; padding: 10px; border-radius: 5px;")
        reset_cart_btn.clicked.connect(self.reset_cart)
        reset_cart_btn.setFixedHeight(40)

        payment_layout.addWidget(pay_whole_btn)
        payment_layout.addWidget(pay_individual_btn)
        payment_layout.addWidget(reset_cart_btn)

        # Make the buttons stretch to fit the width
        payment_layout.addStretch()

        main_layout.addLayout(payment_layout)

    def add_student(self):
        """Add a new student to the cart."""
        student_name = self.student_input.text().strip()

        if not student_name.isalpha() and not all(c.isalpha() or c.isspace() for c in student_name):
            QMessageBox.warning(self, "Invalid Input", "Student name must contain only letters and spaces!")
            return

        if not student_name:
            QMessageBox.warning(self, "Error", "Student name cannot be empty!")
            return

        if student_name in self.students:
            QMessageBox.warning(self, "Error", f"Student '{student_name}' already exists!")
            return

        # Add student and clear input
        self.students.append(student_name)
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
        """Update the shared cart display with products, student details, and delivery fee breakdown."""
        # Clear existing cart items
        while self.cart_layout.count():
            child = self.cart_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self.cart:
            empty_label = QLabel("The cart is empty. Add items to see them here.")
            empty_label.setStyleSheet("color: gray; font-style: italic; margin: 10px;")
            self.cart_layout.addWidget(empty_label)
            return

        # Dictionary to track individual totals (before delivery fee)
        individual_totals = {student: 0 for student in self.students}

        # Organized layout for the cart
        for product_name, product_data in self.cart.items():
            # Product header
            product_header = QLabel(f"{product_name} - ${product_data['price']:.2f}")
            product_header.setStyleSheet("font-weight: bold; margin-top: 10px;")
            self.cart_layout.addWidget(product_header)

            # List of students and quantities for this product
            for student, quantity in product_data["added_by"].items():
                subtotal = product_data["price"] * quantity
                individual_totals[student] += subtotal

                # Display student, quantity, and subtotal
                student_info = QLabel(f"{student}: {quantity} x ${product_data['price']:.2f} = ${subtotal:.2f}")
                student_info.setStyleSheet("margin-left: 15px;")
                self.cart_layout.addWidget(student_info)

                # Remove button for this student-product combination
                remove_button = QPushButton("Remove")
                remove_button.setStyleSheet("margin-left: 10px; padding: 3px; background-color: #E74C3C; color: white;")
                remove_button.clicked.connect(lambda _, p=product_name, s=student: self.remove_product(p, s))
                self.cart_layout.addWidget(remove_button)

        # Calculate and display delivery fee per student
        contributing_students = [s for s, total in individual_totals.items() if total > 0]
        if contributing_students:
            delivery_fee_per_student = self.delivery_fee / len(contributing_students)
            for student in contributing_students:
                individual_totals[student] += delivery_fee_per_student

        # Display individual totals with delivery fee
        total_label = QLabel("\nIndividual Totals (including delivery fee):")
        total_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        self.cart_layout.addWidget(total_label)

        for student, total in individual_totals.items():
            delivery_fee_info = f"(including ${delivery_fee_per_student:.2f} delivery fee)" if student in contributing_students else ""
            total_info = QLabel(f"{student}: ${total:.2f} {delivery_fee_info}")
            self.cart_layout.addWidget(total_info)

    def add_product(self, product):
        """Add a product to the cart, updating the cart display."""
        if self.selected_student is None:
            QMessageBox.warning(self, "Error", "Please select a student first!")
            return

        if product["name"] not in self.cart:
            self.cart[product["name"]] = {
                "price": product["price"],
                "added_by": {self.selected_student: 1}
            }
        else:
            if self.selected_student not in self.cart[product["name"]]["added_by"]:
                self.cart[product["name"]]["added_by"][self.selected_student] = 1
            else:
                self.cart[product["name"]]["added_by"][self.selected_student] += 1

        self.update_cart_display()

    def remove_product(self, product_name, student_name):
        """Remove a product from a student's cart."""
        if product_name in self.cart and student_name in self.cart[product_name]["added_by"]:
            del self.cart[product_name]["added_by"][student_name]
            if not self.cart[product_name]["added_by"]:
                del self.cart[product_name]
            self.update_cart_display()

            

    def pay_whole_cart(self):
        if not self.cart:
            QMessageBox.warning(self, "Oops!", "The cart is empty!")
            return

        grand_total = 0
        for product_name, product_data in self.cart.items():
            for student, quantity in product_data["added_by"].items():
                grand_total += product_data["price"] * quantity

        grand_total += self.delivery_fee
        QMessageBox.information(self, "Ready to Pay!", f"The grand total is ${grand_total:.2f} for everyone!")
    
    def pay_individual(self):
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

    # Display the breakdown
        payment_info = "\n".join([f"{student}: ${total:.2f}" for student, total in payments.items() if total > 0])
        QMessageBox.information(self, "Payment Breakdown", f"Each student's share:\n{payment_info}")

    def reset_cart(self):
        """Reset the cart, student dropdown, and all selections."""
        # Clear the cart
        self.cart.clear()

         # Clear students list and reset dropdown
        self.student_dropdown.blockSignals(True)
        self.students.clear()
        self.student_dropdown.clear()
        self.student_dropdown.addItem("-- Select Student --")
        self.student_dropdown.blockSignals(False)

    # Reset selected student
        self.selected_student = None

    # Clear cart display
        self.update_cart_display()
        QMessageBox.information(self, "Reset", "The cart has been reset. You may enter a new order")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SharedGroceriesCart()
    window.show()
    sys.exit(app.exec())
