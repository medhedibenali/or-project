import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QHBoxLayout, QLineEdit, QLabel, QTabWidget, QHeaderView

from src.pl.read_files import load_products, load_resources, add_product


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.product_columns = ['Name', 'Selling Price', 'Human Work Time', 'Machine Time', 'Resources Needed']
        self.products = load_products()
        self.resources = load_resources()

        self.setWindowTitle('Dynamic Production Planner')
        self.setGeometry(100, 100, 1000, 600)
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create tabs
        self.product_management_tab = QWidget()
        self.resource_management_tab = QWidget()
        self.tab_widget.addTab(self.product_management_tab, "Product Management")
        self.tab_widget.addTab(self.resource_management_tab, "Resource Management")

        # Initialize UI Components for Each Tab
        self.setup_product_management_tab()
        self.setup_resource_management_tab()
        self.load_data_into_ui()

    def add_product_to_table(self, product):
        row_position = self.product_table.rowCount()
        self.product_table.insertRow(row_position)
        print(product)
        # Assuming product dictionary has keys corresponding to table columns
        self.product_table.setItem(row_position, 0, QTableWidgetItem(product['name']))
        self.product_table.setItem(row_position, 1, QTableWidgetItem(product['selling_price']))
        self.product_table.setItem(row_position, 2, QTableWidgetItem(product['human_work_time']))
        self.product_table.setItem(row_position, 3, QTableWidgetItem(product['machine_time']))
        # self.product_table.setItem(row_position, 4, QTableWidgetItem(product['resources_needed']))

    def add_resource_to_table(self, resource):
        row_position = self.resource_table.rowCount()
        self.resource_table.insertRow(row_position)
        # Assuming resource dictionary has keys corresponding to table columns
        self.resource_table.setItem(row_position, 0,
                                    QTableWidgetItem(resource['name']))
        self.resource_table.setItem(row_position, 1,
                                    QTableWidgetItem(resource['quantity_available']))

    def setup_product_management_tab(self):
        self.product_management_layout = QVBoxLayout(self.product_management_tab)
        self.setup_product_table()
        self.setup_product_form()

    def setup_product_table(self):
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(len(self.product_columns))
        self.product_table.setHorizontalHeaderLabels(self.product_columns)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.product_management_layout.addWidget(self.product_table)

    def setup_resource_management_tab(self):
        self.resource_management_layout = QVBoxLayout(self.resource_management_tab)
        self.setup_resource_table()
        self.setup_resource_form()

    def setup_product_form(self):
        # Form layout
        self.product_form_layout = QHBoxLayout()
        self.product_management_layout.addLayout(self.product_form_layout)

        # Form fields
        self.name_input = QLineEdit()
        self.selling_price_input = QLineEdit()
        self.cost_input = QLineEdit()
        self.human_work_time_input = QLineEdit()
        self.machine_time_input = QLineEdit()
        self.resources_needed_input = QLineEdit()

        self.product_form_layout.addWidget(QLabel('Name:'))
        self.product_form_layout.addWidget(self.name_input)

        self.product_form_layout.addWidget(QLabel('Selling Price:'))
        self.product_form_layout.addWidget(self.selling_price_input)

        self.product_form_layout.addWidget(QLabel('Human Work Time:'))
        self.product_form_layout.addWidget(self.human_work_time_input)

        self.product_form_layout.addWidget(QLabel('Machine Time:'))
        self.product_form_layout.addWidget(self.machine_time_input)

        self.product_form_layout.addWidget(QLabel('Resources Needed:'))
        self.product_form_layout.addWidget(self.resources_needed_input)

        # Add and Delete buttons
        self.add_button = QPushButton('Add Product')
        self.add_button.clicked.connect(self.add_product)
        self.product_management_layout.addWidget(self.add_button)

        self.delete_button = QPushButton('Delete Selected Product')
        self.delete_button.clicked.connect(self.delete_product)
        self.product_management_layout.addWidget(self.delete_button)

        # Placeholder for Optimization button (Gurobi integration)
        self.optimize_button = QPushButton('Optimize Production Plan')
        self.optimize_button.clicked.connect(self.optimize_production_plan)
        self.product_management_layout.addWidget(self.optimize_button)

    def setup_resource_table(self):
        self.resource_table = QTableWidget()
        self.resource_table.setColumnCount(2)
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

    def load_data_into_ui(self):
        self.products = load_products()
        self.resources = load_resources()
        print(self.products)

        # Clear existing rows in the tables
        self.product_table.setRowCount(0)
        self.resource_table.setRowCount(0)
        # Populate product table
        for product in self.products:
            self.add_product_to_table(product)

        # Populate resource table
        for resource in self.resources:
            self.add_resource_to_table(resource)

    def add_product(self):
        row_position = self.product_table.rowCount()
        self.product_table.insertRow(row_position)

        self.product_table.setItem(row_position, 0, QTableWidgetItem(self.name_input.text()))
        self.product_table.setItem(row_position, 1, QTableWidgetItem(self.selling_price_input.text()))
        self.product_table.setItem(row_position, 2, QTableWidgetItem(self.human_work_time_input.text()))
        self.product_table.setItem(row_position, 3, QTableWidgetItem(self.machine_time_input.text()))
        self.product_table.setItem(row_position, 4, QTableWidgetItem(self.resources_needed_input.text()))

        new_product = {"name": self.name_input.text(), "selling_price": self.selling_price_input.text(),
                       "human_work_time": self.human_work_time_input.text(),
                       "machine_time": self.machine_time_input.text(),
                       # TODO: Change this to properly handle the different resources and their quantities
                       "resources_needed": self.resources_needed_input.text().split(',')}
        add_product(new_product)

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
        # Here we will collect data from the table and use Gurobi for optimization.
        # This function currently serves as a placeholder.
        print("Optimization placeholder. This is where the Gurobi optimization logic will be implemented.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
