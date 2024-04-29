from typing import List, Set
import gurobipy as gp
from gurobipy import GRB


class InitializationException(RuntimeError):
    def __init__(self, message, location) -> None:
        super().__init__(message)
        self.location = location


class OptimizationException(RuntimeError):
    def __init__(self, message) -> None:
        super().__init__(message)


class PlneOptimizer:
    def __init__(self, start, finish, graph):
        self.model = gp.Model("Shortest Path")

        self.verify_node(start, "start")
        self.verify_node(finish, "finish")

        if start == finish:
            raise InitializationException(
                "The finish can't be the same as the start.", "finish"
            )

        self.start = start
        self.finish = finish

        self.graph = graph

        self.initialize()

    def optimize(self):
        self.prepare_model()
        self.model.optimize()

        if self.model.Status != GRB.OPTIMAL:
            raise OptimizationException(
                "Could not find a path from the start to the finish with the given graph."
            )

        return self.get_result()

    def prepare_model(self):
        self.x = self.model.addVars(self.edges_count, vtype=GRB.BINARY, name="edge")
        self.y = self.model.addVars(
            self.nodes_count - 2, vtype=GRB.BINARY, name="visit"
        )

        self.model.setObjective(
            gp.quicksum(self.x[i] * self.costs[i] for i in range(self.edges_count)),
            GRB.MINIMIZE,
        )

        self.model.addConstrs(
            (gp.quicksum(self.x[i] for i in self.edges[j]) == 1 for j in range(2)),
            name="bound",
        )

        self.model.addConstrs(
            (
                (
                    (self.y[j - 2] == k)
                    >> (gp.quicksum(self.x[i] for i in self.edges[j]) == 2 * k)
                )
                for j in range(2, self.nodes_count)
                for k in range(2)
            ),
            name="middle",
        )

    def get_result(self):
        self.objective_value = self.model.ObjVal

        self.path_edges = {
            i
            for (i, x) in enumerate(self.model.getVars())
            if x.varName.startswith("edge") and (x.X == 1)
        }

        self.path_edges_sorted = []
        self.path_nodes = []

        node = self.start
        node_index = self.indexes[node]

        node_edges = set()

        for _ in range(len(self.path_edges)):
            edge = ((self.edges[node_index] & self.path_edges) - node_edges).pop()

            self.path_edges_sorted.append(edge)
            self.path_nodes.append(node)

            node1, node2, _ = self.graph[edge]

            if node == node1:
                node = node2
            else:
                node = node1

            node_index = self.indexes[node]

            node_edges = {edge}

        self.path_nodes.append(node)

        return (self.objective_value, self.path_edges_sorted, self.path_nodes)

    def initialize(self):
        self.indexes = {self.start: 0, self.finish: 1}

        self.costs: List[float] = []

        self.nodes_count = 2
        self.nodes: List[Set[int]] = [set(), set()]
        self.edges: List[Set[int]] = [set(), set()]

        for edge, (node1, node2, cost) in enumerate(self.graph):
            self.verify_node(node1, edge)
            self.verify_node(node2, edge)

            try:
                v = float(cost)

                if v <= 0:
                    raise ValueError()

                self.costs.append(v)
            except ValueError:
                raise InitializationException(
                    "The cost must be a valid strictly positive number.", edge
                )

            i = self.update_edges(node1, edge)
            j = self.update_edges(node2, edge)

            self.update_nodes(i, j, edge)

        self.edges_count = len(self.costs)

    def update_edges(self, node, edge):
        i = self.indexes.get(node)

        if i == None:
            i = self.nodes_count
            self.nodes_count += 1
            self.indexes[node] = i

            self.edges.append({edge})
            self.nodes.append(set())
        else:
            self.edges[i].add(edge)

        return i

    def verify_node(self, node, location):
        node_name = str(node)
        if (not node_name) or (node_name.strip() != node_name):
            raise InitializationException(
                "A node's name can't have extra spaces or be empty.", location
            )

    def update_nodes(self, node1, node2, edge):
        if node1 == node2:
            raise InitializationException(
                "Can't have an edge that links a node to itself.", edge
            )

        if node2 < node1:
            (node1, node2) = (node2, node1)

        if node2 in self.nodes[node1]:
            raise InitializationException(
                "Can't have more than one edge that links two nodes together.", edge
            )

        self.nodes[node1].add(node2)


if __name__ == "__main__":
    start = "start"
    finish = "finish"
    graph = [
        ("start", 2, 3),
        (2, "finish", 5),
        ("start", "finish", 10),
        (2, 4, 1),
        (4, 5, 1),
        (5, "finish", 1),
    ]

    try:
        optimizer = PlneOptimizer(start, finish, graph)

        objective_value, edges, nodes = optimizer.optimize()
        print("\nobjective value: ", objective_value)

        output = f"{edges[0]}"

        print("\nedges")
        for i in range(1, len(edges)):
            output = f"{output} -> {edges[i]}"

        print(output)

        output = f"{nodes[0]}"

        print("\nnodes")
        for i in range(1, len(nodes)):
            output = f"{output} -> {nodes[i]}"

        print(output)

    except InitializationException as e:
        print(e, e.location)
    except OptimizationException as e:
        print(e)
