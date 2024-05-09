import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QHBoxLayout, QLineEdit, QLabel, QTabWidget, QHeaderView, QDialog,
                             QDoubleSpinBox, QSpinBox)

from src.pl.ResourceManagementDialog import ResourceManagementDialog
from src.pl.optimizer import PlOptimizer
from src.pl.read_files import load_products, load_resources, add_product, add_resource, load_human_machine_time, \
    add_human_machine_time
from src.styles import Styles


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.font = QFont(Styles.FONT_TYPE)
        self.setFont(self.font)

        self.product_columns = ["Name", "Selling Price", "Human Work Time", "Machine Time"]
        self.products = load_products()
        self.human_machine_time_columns = ["Human work time", "Machine work time"]
        self.human_machine_time = load_human_machine_time()
        self.resources = load_resources()
        self.current_product = None
        self.setWindowTitle("Dynamic Production Planner")
        self.setGeometry(100, 100, 1000, 600)
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create tabs
        self.product_management_tab = QWidget()
        self.resource_management_tab = QWidget()
        self.human_machine_time_management_tab = QWidget()
        self.tab_widget.addTab(self.product_management_tab, "Product Management")
        self.tab_widget.addTab(self.resource_management_tab, "Resource Management")
        self.tab_widget.addTab(self.human_machine_time_management_tab, "Work time Management")

        # Initialize UI Components for Each Tab
        self.setup_product_management_tab()
        self.setup_resource_management_tab()
        self.setup_human_machine_management_tab()

        self.load_data_into_ui()

    def add_product_to_table(self, product):
        row_position = self.product_table.rowCount()
        self.product_table.insertRow(row_position)
        self.product_table.setItem(row_position, 0, QTableWidgetItem(product["name"]))
        self.product_table.setItem(row_position, 1, QTableWidgetItem(str(product["selling_price"])))
        self.product_table.setItem(row_position, 2, QTableWidgetItem(str(product["human_work_time"])))
        self.product_table.setItem(row_position, 3, QTableWidgetItem(str(product["machine_time"])))

    def add_human_machine_time_to_table(self, human_machine_time):
        row_position = self.product_table.rowCount()
        self.product_table.insertRow(row_position)
        self.product_table.setItem(row_position, 0, QTableWidgetItem(str(human_machine_time["human_time"])))
        self.product_table.setItem(row_position, 1, QTableWidgetItem(str(human_machine_time["machine_time"])))

    def add_resource_to_table(self, resource):
        row_position = self.resource_table.rowCount()
        self.resource_table.insertRow(row_position)
        # Convert numerical values to strings before setting them as table items
        self.resource_table.setItem(row_position, 0, QTableWidgetItem(resource["name"]))
        self.resource_table.setItem(row_position, 1, QTableWidgetItem(str(resource["quantity_available"])))

    def setup_product_management_tab(self):
        self.product_management_layout = QVBoxLayout(self.product_management_tab)
        self.setup_product_table()
        self.setup_product_form()
        self.update_button_state(self.product_fields, self.add_button, "Please fill in all fields to add a product.")

    def setup_product_table(self):
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(len(self.product_columns))
        self.product_table.setHorizontalHeaderLabels(self.product_columns)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.product_management_layout.addWidget(self.product_table)

    def setup_human_machine_management_tab(self):
        self.human_machine_time_management_layout = QVBoxLayout(self.human_machine_time_management_tab)
        self.setup_human_machine_table()
        self.setup_human_machine_form()
        self.human_machine_fields = [self.human_time_input, self.machine_time_input]
        self.update_button_state(self.human_machine_fields, self.add_button, "Please fill in all fields .")

    def setup_human_machine_table(self):
        self.human_machine_table = QTableWidget()
        self.human_machine_table.setColumnCount(len(self.human_machine_time_columns))
        self.human_machine_table.setHorizontalHeaderLabels(self.human_machine_time_columns)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.human_machine_time_management_layout.addWidget(self.human_machine_table)

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
        self.selling_price_input = QDoubleSpinBox()
        self.selling_price_input.setMaximum(999999.99)
        self.human_work_time_input = QSpinBox()
        self.human_work_time_input.setMaximum(999999)
        self.machine_time_input = QSpinBox()
        self.machine_time_input.setMaximum(999999)

        self.product_fields = [self.name_input, self.selling_price_input, self.human_work_time_input,
                               self.machine_time_input]

        # Connect each field's textChanged signal
        for field in self.product_fields:
            field.textChanged.connect(lambda: self.update_button_state(self.product_fields, self.add_button,
                                                                       "Please fill in all fields to add a product."))

        self.product_form_layout.addWidget(QLabel("Name:"))
        self.product_form_layout.addWidget(self.name_input)

        self.product_form_layout.addWidget(QLabel("Selling Price:"))
        self.product_form_layout.addWidget(self.selling_price_input)

        self.product_form_layout.addWidget(QLabel("Human Work Time:"))
        self.product_form_layout.addWidget(self.human_work_time_input)

        self.product_form_layout.addWidget(QLabel("Machine Time:"))
        self.product_form_layout.addWidget(self.machine_time_input)

        self.manage_resources_btn = QPushButton("Manage Resources")
        self.manage_resources_btn.clicked.connect(self.manage_product_resources)
        self.product_form_layout.addWidget(self.manage_resources_btn)

        # Add and Delete buttons
        self.add_button = QPushButton("Add Product")
        self.add_button.clicked.connect(self.add_product)
        self.product_management_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete Selected Product")
        self.delete_button.clicked.connect(self.delete_product)
        self.product_management_layout.addWidget(self.delete_button)

        self.optimize_button = QPushButton("Optimize Production Plan")
        self.optimize_button.clicked.connect(self.optimize_production_plan)
        self.product_management_layout.addWidget(self.optimize_button)

    def setup_human_machine_form(self):
        # Form layout
        self.human_machine_time_form_layout = QHBoxLayout()
        self.human_machine_time_management_layout.addLayout(self.human_machine_time_form_layout)

        # Form fields
        self.human_time_input = QSpinBox()
        self.machine_time_input = QSpinBox()

        self.human_machine_time_fields = [self.human_time_input, self.machine_time_input]

        # Connect each field's textChanged signal
        for field in self.human_machine_time_fields:
            field.textChanged.connect(lambda: self.update_button_state(self.human_machine_time_fields, self.add_button,
                                                                       "Please fill in all fields ."))

        self.human_machine_time_form_layout.addWidget(QLabel("Human Work Time:"))
        self.human_machine_time_form_layout.addWidget(self.human_time_input)

        self.human_machine_time_form_layout.addWidget(QLabel("Machine work Time:"))
        self.human_machine_time_form_layout.addWidget(self.machine_time_input)

        # Add and Delete buttons
        self.add_human_machine_button = QPushButton('Set work time')
        self.add_button.clicked.connect(self.add_human_machine_time)
        self.human_machine_time_management_layout.addWidget(self.add_human_machine_button)

        # self.delete_button = QPushButton("Delete")
        # self.delete_button.clicked.connect(self.delete_human_machine_time)
        # self.human_machine_time_management_layout.addWidget(self.delete_button)

        # Placeholder for Optimization button (Gurobi integration)
        self.optimize_button = QPushButton("Optimize Production Plan")
        self.optimize_button.clicked.connect(self.optimize_production_plan)
        self.human_machine_time_management_layout.addWidget(self.optimize_button)

    def setup_resource_table(self):
        self.resource_table = QTableWidget()
        self.resource_table.setColumnCount(2)
        self.resource_table.setHorizontalHeaderLabels(["Resource Name", "Quantity Available"])
        self.resource_management_layout.addWidget(self.resource_table)

    def manage_product_resources(self):
        self.current_product = {"name": self.name_input.text(), "selling_price": self.selling_price_input.value(),
                                "human_work_time": self.human_work_time_input.value(),
                                "machine_time": self.machine_time_input.value(), "resources_needed": [], }
        add_product(self.current_product)
        self.resources = load_resources()
        dialog = ResourceManagementDialog(self.resources, self.current_product)
        if dialog.exec_() == QDialog.Accepted:
            # Gather data from dialog and update the product being added/edited
            pass

    def setup_resource_form(self):
        self.resource_form_layout = QHBoxLayout()
        self.resource_management_layout.addLayout(self.resource_form_layout)

        self.resource_name_input = QLineEdit()
        self.quantity_available_input = QSpinBox()
        self.quantity_available_input.setMaximum(99999999)
        self.resource_fields = [self.resource_name_input, self.quantity_available_input]

        for field in self.resource_fields:
            field.textChanged.connect(lambda: self.update_button_state(self.resource_fields, self.add_resource_button,
                                                                       "Please enter a valid name and quantity to add a resource."))

        self.resource_form_layout.addWidget(QLabel("Resource Name:"))
        self.resource_form_layout.addWidget(self.resource_name_input)

        self.resource_form_layout.addWidget(QLabel("Quantity Available:"))
        self.resource_form_layout.addWidget(self.quantity_available_input)

        self.add_resource_button = QPushButton("Add Resource")
        self.add_resource_button.clicked.connect(self.add_resource)
        self.resource_management_layout.addWidget(self.add_resource_button)
        self.update_button_state(self.resource_fields, self.add_resource_button,
                                 "Please enter a valid name and quantity to add a resource.")

        self.delete_resource_button = QPushButton("Delete Selected Resource")
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
        self.product_table.setItem(row_position, 1, QTableWidgetItem(str(self.selling_price_input.value())))
        self.product_table.setItem(row_position, 2, QTableWidgetItem(str(self.human_work_time_input.value())))
        self.product_table.setItem(row_position, 3, QTableWidgetItem(str(self.machine_time_input.value())))

        # FIXME: We removed this to prevent the product being saved twice (here and when adding ressources). See if there's a better way
        # new_product = {"name": self.name_input.text(), "selling_price": self.selling_price_input.text(),
        #                "human_work_time": self.human_work_time_input.text(),
        #                "machine_time": self.machine_time_input.text(), }
        # add_product(new_product)

        # Clear input fields after adding
        self.name_input.clear()
        self.selling_price_input.setValue(0)
        self.human_work_time_input.setValue(0)
        self.machine_time_input.setValue(0)

    def add_resource(self):
        row_position = self.resource_table.rowCount()
        self.resource_table.insertRow(row_position)
        self.resource_table.setItem(row_position, 0, QTableWidgetItem(self.resource_name_input.text()))
        self.resource_table.setItem(row_position, 1, QTableWidgetItem(str(self.quantity_available_input.value())))

        new_resource = {"name": self.resource_name_input.text(),
                        "quantity_available": self.quantity_available_input.value(), }
        add_resource(new_resource)
        self.resource_name_input.clear()
        self.quantity_available_input.setValue(0)

    def add_human_machine_time(self):
        row_position = self.human_machine_table.rowCount()
        self.human_machine_table.insertRow(row_position)
        self.human_machine_table.setItem(row_position, 0, QTableWidgetItem(str(self.human_time_input.value())))
        self.human_machine_table.setItem(row_position, 1, QTableWidgetItem(str(self.machine_time_input.value())))

        new_resource = {"human_time": self.human_time_input.value(), "machine_time": self.machine_time_input.value()}
        add_human_machine_time(new_resource)
        self.human_time_input.clear()
        self.machine_time_input.setValue(0)

    def delete_resource(self):
        indices = self.resource_table.selectionModel().selectedRows()
        for index in sorted(indices, reverse=True):
            self.resource_table.removeRow(index.row())

    def delete_product(self):
        indices = self.product_table.selectionModel().selectedRows()
        for index in sorted(indices, reverse=True):
            self.product_table.removeRow(index.row())

    @staticmethod
    def update_button_state(fields, button, tooltip_message):
        # Check if all the fields are non-empty
        is_all_fields_non_empty = all(field.text().strip() for field in fields)

        # Enable the button if all fields are non-empty, else disable it
        button.setEnabled(is_all_fields_non_empty)

        # Update tooltip based on the button's enabled state
        if not button.isEnabled():
            button.setToolTip(tooltip_message)
        else:
            button.setToolTip("")  # Clear tooltip when the button is enabled

    def optimize_production_plan(self):
        pl_optimizer = PlOptimizer()
        optimized_plan, total_sales = pl_optimizer.optimize()

        result_dialog = QDialog(self)
        result_layout = QVBoxLayout(result_dialog)

        result_table = QTableWidget()
        result_table.setColumnCount(2)
        result_table.setHorizontalHeaderLabels(["Product", "Optimized Quantity"])

        result_table.setMinimumSize(400, 300)
        result_dialog.setMinimumSize(450, 350)

        sorted_optimized_plan = dict(sorted(optimized_plan.items(), key=lambda item: item[1], reverse=True))
        for product, quantity in sorted_optimized_plan.items():
            row_position = result_table.rowCount()
            result_table.insertRow(row_position)
            result_table.setItem(row_position, 0, QTableWidgetItem(product))
            result_table.setItem(row_position, 1, QTableWidgetItem(f"{quantity:,.0f}"))
        result_layout.addWidget(result_table)
        result_layout.addWidget(QLabel(f"Total Projected Sales: ${total_sales:,.2f}"))
        result_dialog.setLayout(result_layout)
        result_dialog.setWindowTitle("Optimization Results")
        result_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
