import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget,
                             QHBoxLayout, QScrollArea, QTextEdit, )

from src.plne.optimizer import PlneOptimizer, InitializationException, OptimizationException
from src.styles import Styles

class NodePairWidget(QWidget):
    def __init__(self):
        super(NodePairWidget, self).__init__()

        layout = QHBoxLayout()


        self.node1_label = QLabel("Node 1:")
        self.node1_input = QLineEdit()
        self.node1_label.setFont(QFont(Styles.FONT_TYPE, 12))
        self.node1_input.setFont(QFont(Styles.FONT_TYPE, 12))
        layout.addWidget(self.node1_label)
        layout.addWidget(self.node1_input)
        self.node1_input.setStyleSheet(
            "border: none; background-color: %s; border-radius: 5px; margin: 0 8px 0 4px;" % Styles.LIGHT_BG_COLOR)
        self.node1_label.setStyleSheet("color: %s" % Styles.LABEL_COLOR)

        self.node2_label = QLabel("Node 2:")
        self.node2_input = QLineEdit()
        self.node2_label.setFont(QFont(Styles.FONT_TYPE, 12))
        self.node2_input.setFont(QFont(Styles.FONT_TYPE, 12))
        layout.addWidget(self.node2_label)
        layout.addWidget(self.node2_input)
        self.node2_input.setStyleSheet(
            "border: none; background-color: %s; border-radius: 5px; margin: 0 8px 0 4px;" % Styles.LIGHT_BG_COLOR)
        self.node2_label.setStyleSheet("color: %s" % Styles.LABEL_COLOR)

        self.cost_label = QLabel("Cost:")
        self.cost_input = QLineEdit()
        self.cost_label.setFont(QFont(Styles.FONT_TYPE, 12))
        self.cost_input.setFont(QFont(Styles.FONT_TYPE, 12))
        layout.addWidget(self.cost_label)
        layout.addWidget(self.cost_input)
        self.cost_input.setStyleSheet(
            "border: none; background-color: %s; border-radius: 5px; margin: 0 8px 0 4px;" % Styles.LIGHT_BG_COLOR)
        self.cost_label.setStyleSheet("color: %s;" % Styles.LABEL_COLOR)

        self.remove_button = QPushButton("Remove")
        self.remove_button.setStyleSheet(
            "font-size: 12px; background-color: %s; color: %s; border: none; padding: 5px 10px; border-radius: 5px; margin: 0 16px;" % (
                Styles.REMOVE_BUTTON_COLOR, Styles.BUTTON_TEXT_COLOR))
        layout.addWidget(self.remove_button)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.resize(800, 700)
        self.setStyleSheet("background-color: %s;" % Styles.WINDOW_BACKGROUND_COLOR)

        self.source_label = QLabel("Source Node:")
        self.source_input = QLineEdit()
        self.source_label.setFont(QFont(Styles.FONT_TYPE, 14))
        self.source_input.setFont(QFont(Styles.FONT_TYPE, 14))
        self.source_input.setStyleSheet("color: %s; border-radius: 5px;" % Styles.INPUT_TEXT_COLOR)
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_input)
        self.source_label.setStyleSheet("color: %s;" % Styles.BIG_LABEL_COLOR)
        self.source_input.setStyleSheet("border: none; background-color: %s; border-radius: 5px; color: %s;" % (
            Styles.NODE_PAIR_BACKGROUND_COLOR, Styles.INPUT_TEXT_COLOR))

        self.dest_label = QLabel("Destination Node:")
        self.dest_input = QLineEdit()
        self.dest_label.setFont(QFont(Styles.FONT_TYPE, 14))
        self.dest_input.setFont(QFont(Styles.FONT_TYPE, 14))
        self.dest_input.setStyleSheet("color: %s; border-radius: 5px;" % Styles.INPUT_TEXT_COLOR)
        layout.addWidget(self.dest_label)
        layout.addWidget(self.dest_input)
        self.dest_label.setStyleSheet("color: %s;" % Styles.BIG_LABEL_COLOR)
        self.dest_input.setStyleSheet("border: none; background-color: %s; border-radius: 5px;  color: %s;" % (
            Styles.NODE_PAIR_BACKGROUND_COLOR, Styles.INPUT_TEXT_COLOR))

        self.node_pairs_label = QLabel("Node Pairs and Costs:")
        self.node_pairs_label.setFont(QFont(Styles.FONT_TYPE, 14))
        self.node_pairs_label.setStyleSheet("color: %s; border: none;" % Styles.BIG_LABEL_COLOR)
        layout.addWidget(self.node_pairs_label)

        # Create a scroll area for node pairs
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)

        self.node_pair_container = QWidget()
        self.node_pair_layout = QVBoxLayout()
        self.node_pair_container.setLayout(self.node_pair_layout)
        scroll_widget.setStyleSheet("background-color: %s; border: none;" % Styles.NODE_PAIR_BACKGROUND_COLOR)

        # Set alignment of node pair container to top
        self.node_pair_layout.setAlignment(Qt.AlignTop)

        # Add node pair container to the scroll widget
        scroll_layout.addWidget(self.node_pair_container)

        # Set scroll widget as the widget of the scroll area
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)  # Make scroll area resizable

        layout.addWidget(scroll_area)

        self.add_node_pair_button = QPushButton("+ Add Node Pair")
        self.add_node_pair_button.setStyleSheet(
            "font-size: 14px; background-color: %s; color: %s; border: none; padding: 10px 20px; border-radius: 5px;" % (
                Styles.ADD_BUTTON_COLOR, Styles.BUTTON_TEXT_COLOR))
        layout.addWidget(self.add_node_pair_button)

        self.calculate_button = QPushButton("Calculate Shortest Path")
        self.calculate_button.setStyleSheet(
            "font-size: 14px; background-color: %s; color: %s; border: none; padding: 10px 20px; border-radius: 5px;" % (
                Styles.CALCULATE_BUTTON_COLOR, Styles.BUTTON_TEXT_COLOR))
        layout.addWidget(self.calculate_button)

        self.node_pair_inputs = []

        self.add_node_pair_button.clicked.connect(self.add_node_pair)
        self.calculate_button.clicked.connect(self.calculate_shortest_path)

        self.result_container = QWidget()
        self.result_layout = QVBoxLayout()
        self.result_container.setLayout(self.result_layout)
        self.result_layout.setAlignment(Qt.AlignTop)
        self.result_container.setStyleSheet("background-color: %s; border: none;" % Styles.NODE_PAIR_BACKGROUND_COLOR)

        self.result_label = QLabel()
        self.result_label.setText("Output:")
        self.result_label.setFont(QFont(Styles.FONT_TYPE, 14))
        self.result_label.setStyleSheet("color: %s" % Styles.LABEL_COLOR)
        self.result_layout.addWidget(self.result_label)
        self.result_container.setFixedHeight(150)
        layout.addWidget(self.result_container)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)  # Make it read-only
        self.result_area.setFont(QFont(Styles.FONT_TYPE, 12))  # Set font
        self.result_area.setStyleSheet("color: %s" % Styles.LABEL_COLOR)
        self.result_layout.addWidget(self.result_area)  # Add result_area to result_layout

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

        try:
            optimizer = PlneOptimizer(source, dest, node_pairs)

            objective_value, edges, nodes = optimizer.optimize()

            self.result_area.clear()
            print("\nobjective value: ", objective_value)
            self.result_area.append(f"Objective value: {objective_value}")

            output = f"{edges[0]}"
            print("\nedges")
            self.result_area.append("Edges:")
            for i in range(1, len(edges)):
                output = f"{output} -> {edges[i]}"
            print(output)
            self.result_area.append(output)

            output = f"{nodes[0]}"
            print("\nnodes")
            self.result_area.append("Nodes:")
            for i in range(1, len(nodes)):
                output = f"{output} -> {nodes[i]}"
            print(output)
            self.result_area.append(output)

        except InitializationException as e:
            print(e, e.location)
            self.result_area.clear()
            self.result_area.append(f"Error: {e}")
            self.result_area.append(f"At: {e.location}")

        except OptimizationException as e:
            print(e)
            self.result_area.clear()
            self.result_area.append(f"Error: {e}")




def main():
    app = QApplication(sys.argv)
    main_app = MainWindow()
    main_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
