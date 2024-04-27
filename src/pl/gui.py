import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QLabel, QTabWidget


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dynamic Production Planner')
        self.setGeometry(100, 100, 1000, 600)
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        # self.layout = QVBoxLayout()
        # self.central_widget.setLayout(self.layout)
        # self.setup_product_table()
        # self.setup_product_form()

        # Create tabs
        self.product_management_tab = QWidget()
        self.resource_management_tab = QWidget()
        self.tab_widget.addTab(self.product_management_tab, "Product Management")
        self.tab_widget.addTab(self.resource_management_tab, "Resource Management")

        # Initialize UI Components for Each Tab
        self.setup_product_management_tab()
        self.setup_resource_management_tab()

    def setup_product_management_tab(self):
        # Creating a layout for the product_management_tab
        product_management_layout = QVBoxLayout()
        self.product_management_tab.setLayout(product_management_layout)  # Set this layout on the tab

        self.setup_product_table(product_management_layout)  # Pass the layout to the method

    def setup_product_table(self, layout):  # Accept the layout as a parameter
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(6)  # Example setup
        self.product_table.setHorizontalHeaderLabels(
            ['Name', 'Selling Price', 'Cost', 'Human Work Time', 'Machine Time', 'Resources Needed'])

        layout.addWidget(self.product_table)  # Use the passed layout here

    def setup_resource_management_tab(self):
        self.resource_management_layout = QVBoxLayout(self.resource_management_tab)
        self.setup_resource_table()
        self.setup_resource_form()

    def setup_product_form(self):
        # Form layout
        self.form_layout = QHBoxLayout()
        self.layout.addLayout(self.form_layout)

        # Form fields
        self.name_input = QLineEdit()
        self.selling_price_input = QLineEdit()
        self.cost_input = QLineEdit()
        self.human_work_time_input = QLineEdit()
        self.machine_time_input = QLineEdit()
        self.resources_needed_input = QLineEdit()

        self.form_layout.addWidget(QLabel('Name:'))
        self.form_layout.addWidget(self.name_input)

        self.form_layout.addWidget(QLabel('Selling Price:'))
        self.form_layout.addWidget(self.selling_price_input)

        self.form_layout.addWidget(QLabel('Cost:'))
        self.form_layout.addWidget(self.cost_input)

        self.form_layout.addWidget(QLabel('Human Work Time:'))
        self.form_layout.addWidget(self.human_work_time_input)

        self.form_layout.addWidget(QLabel('Machine Time:'))
        self.form_layout.addWidget(self.machine_time_input)

        self.form_layout.addWidget(QLabel('Resources Needed:'))
        self.form_layout.addWidget(self.resources_needed_input)

        # Add and Delete buttons
        self.add_button = QPushButton('Add Product')
        self.add_button.clicked.connect(self.add_product)
        self.layout.addWidget(self.add_button)

        self.delete_button = QPushButton('Delete Selected Product')
        self.delete_button.clicked.connect(self.delete_product)
        self.layout.addWidget(self.delete_button)

        # Placeholder for Optimization button (Gurobi integration)
        self.optimize_button = QPushButton('Optimize Production Plan')
        self.optimize_button.clicked.connect(self.optimize_production_plan)
        self.layout.addWidget(self.optimize_button)

    def setup_resource_table(self):
        self.resource_table = QTableWidget()
        self.resource_table.setColumnCount(2)  # Adjust based on attributes
        self.resource_table.setHorizontalHeaderLabels(['Resource Name', 'Quantity Available'])
        self.resource_management_layout.addWidget(self.resource_table)

    def setup_resource_form(self):
        self.resource_form_layout = QHBoxLayout()
        self.resource_management_layout.addLayout(self.resource_form_layout)

        self.resource_name_input = QLineEdit()
        self.quantity_available_input = QLineEdit()

        self.resource_form_layout.addWidget(QLabel('Resource Name:'))
        self.resource_form_layout.addWidget(self.resource_name_input)

        self.resource_form_layout.addWidget(QLabel('Quantity Available:'))
        self.resource_form_layout.addWidget(self.quantity_available_input)

        self.add_resource_button = QPushButton('Add Resource')
        self.add_resource_button.clicked.connect(self.add_resource)
        self.resource_management_layout.addWidget(self.add_resource_button)

        self.delete_resource_button = QPushButton('Delete Selected Resource')
        self.delete_resource_button.clicked.connect(self.delete_resource)
        self.resource_management_layout.addWidget(self.delete_resource_button)

        # Additional functions for adding and deleting resources go here

    def add_product(self):
        row_position = self.product_table.rowCount()
        self.product_table.insertRow(row_position)

        self.product_table.setItem(row_position, 0, QTableWidgetItem(self.name_input.text()))
        self.product_table.setItem(row_position, 1, QTableWidgetItem(self.selling_price_input.text()))
        self.product_table.setItem(row_position, 2, QTableWidgetItem(self.cost_input.text()))
        self.product_table.setItem(row_position, 3, QTableWidgetItem(self.human_work_time_input.text()))
        self.product_table.setItem(row_position, 4, QTableWidgetItem(self.machine_time_input.text()))
        self.product_table.setItem(row_position, 5, QTableWidgetItem(self.resources_needed_input.text()))

        # Clear input fields after adding
        self.name_input.clear()
        self.selling_price_input.clear()
        self.cost_input.clear()
        self.human_work_time_input.clear()
        self.machine_time_input.clear()
        self.resources_needed_input.clear()

    def add_resource(self):
        row_position = self.resource_table.rowCount()
        self.resource_table.insertRow(row_position)
        self.resource_table.setItem(row_position, 0, QTableWidgetItem(self.resource_name_input.text()))
        self.resource_table.setItem(row_position, 1, QTableWidgetItem(self.quantity_available_input.text()))
        self.resource_name_input.clear()
        self.quantity_available_input.clear()

    def delete_resource(self):
        indices = self.resource_table.selectionModel().selectedRows()
        for index in sorted(indices, reverse=True):
            self.resource_table.removeRow(index.row())

    def delete_product(self):
        indices = self.product_table.selectionModel().selectedRows()
        for index in sorted(indices, reverse=True):
            self.product_table.removeRow(index.row())

    def optimize_production_plan(self):
        # Here you will collect data from the table and use Gurobi for optimization.
        # This function currently serves as a placeholder.
        print("Optimization placeholder. This is where the Gurobi optimization logic will be implemented.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
