import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout


class NodePairWidget(QWidget):
    def __init__(self):
        super(NodePairWidget, self).__init__()

        layout = QHBoxLayout()

        self.node1_label = QLabel("Node 1:")
        self.node1_input = QLineEdit()
        layout.addWidget(self.node1_label)
        layout.addWidget(self.node1_input)

        self.node2_label = QLabel("Node 2:")
        self.node2_input = QLineEdit()
        layout.addWidget(self.node2_label)
        layout.addWidget(self.node2_input)

        self.cost_label = QLabel("Cost:")
        self.cost_input = QLineEdit()
        layout.addWidget(self.cost_label)
        layout.addWidget(self.cost_input)

        self.remove_button = QPushButton("Remove")
        layout.addWidget(self.remove_button)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.source_label = QLabel("Source Node:")
        self.source_input = QLineEdit()
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_input)

        self.dest_label = QLabel("Destination Node:")
        self.dest_input = QLineEdit()
        layout.addWidget(self.dest_label)
        layout.addWidget(self.dest_input)

        self.node_pairs_label = QLabel("Node Pairs and Costs:")
        layout.addWidget(self.node_pairs_label)

        self.node_pair_container = QWidget()
        self.node_pair_layout = QVBoxLayout()
        self.node_pair_container.setLayout(self.node_pair_layout)
        layout.addWidget(self.node_pair_container)

        self.add_node_pair_button = QPushButton("+ Add Node Pair")
        layout.addWidget(self.add_node_pair_button)

        self.calculate_button = QPushButton("Calculate Shortest Path")
        layout.addWidget(self.calculate_button)

        self.node_pair_inputs = []

        self.add_node_pair_button.clicked.connect(self.add_node_pair)
        self.calculate_button.clicked.connect(self.calculate_shortest_path)

    def add_node_pair(self):
        node_pair_widget = NodePairWidget()
        self.node_pair_layout.addWidget(node_pair_widget)
        self.node_pair_inputs.append(node_pair_widget)
        node_pair_widget.remove_button.clicked.connect(lambda _, widget=node_pair_widget: self.remove_node_pair(widget))

    def remove_node_pair(self, widget):
        if widget in self.node_pair_inputs:
            self.node_pair_inputs.remove(widget)
            self.node_pair_layout.removeWidget(widget)
            widget.deleteLater()

    def calculate_shortest_path(self):
        source = self.source_input.text()
        dest = self.dest_input.text()

        node_pairs = []
        for node_pair_widget in self.node_pair_inputs:
            node1 = node_pair_widget.node1_input.text()
            node2 = node_pair_widget.node2_input.text()
            cost = node_pair_widget.cost_input.text()

            # Check if any field is empty, if so, skip this pair
            if node1.strip() and node2.strip() and cost.strip():
                node_pairs.append((node1, node2, cost))
            else:
                print("Error: Incomplete node pair")

        print("Source Node:", source)
        print("Destination Node:", dest)
        print("Node Pairs and Costs:")
        for node1, node2, cost in node_pairs:
            print("Node 1:", node1, "| Node 2:", node2, "| Cost:", cost)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
