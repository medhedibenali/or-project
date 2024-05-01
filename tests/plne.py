import unittest
import random

import networkx as nx

from src.plne.optimizer import (
    InitializationException,
    OptimizationException,
    PlneOptimizer,
)


def generate_graph(n=100, p=0.3, min_weight=1.0, max_weight=10.0):
    G = nx.erdos_renyi_graph(n, p)

    weights = {
        edge: {"weight": random.uniform(min_weight, max_weight)} for edge in G.edges
    }
    nx.set_edge_attributes(G, weights)

    graph = [
        (node1, node2, attributes["weight"])
        for ((node1, node2), attributes) in weights.items()
    ]

    start, finish = random.sample(list(G.nodes), 2)

    return start, finish, graph, G


class TestPlneOptimizer(unittest.TestCase):
    def test_invalid_start(self):
        start = ""
        finish = "finish"
        graph = []

        with self.assertRaises(InitializationException):
            PlneOptimizer(start, finish, graph)

    def test_invalid_finish(self):
        start = "start"
        finish = ""
        graph = []

        with self.assertRaises(InitializationException):
            PlneOptimizer(start, finish, graph)

    def test_same_start_and_finish(self):
        start = "start"
        finish = "start"
        graph = []

        with self.assertRaises(InitializationException):
            PlneOptimizer(start, finish, graph)

    def test_invalid_node(self):
        start = "start"
        finish = "finish"
        graph = [("", finish, 1)]

        with self.assertRaises(InitializationException):
            PlneOptimizer(start, finish, graph)

    def test_invalid_cost(self):
        start = "start"
        finish = "finish"
        graph = [(start, finish, "a")]

        with self.assertRaises(InitializationException):
            PlneOptimizer(start, finish, graph)

    def test_invalid_cost_value(self):
        start = "start"
        finish = "finish"
        graph = [(start, finish, "0")]

        with self.assertRaises(InitializationException):
            PlneOptimizer(start, finish, graph)

    def test_self_loop(self):
        start = "start"
        finish = "finish"
        graph = [(start, start, "1")]

        with self.assertRaises(InitializationException):
            optimizer = PlneOptimizer(start, finish, graph)
            optimizer.optimize()

    def test_duplicate_edge(self):
        start = "start"
        finish = "finish"
        graph = [(start, "a", "1"), (start, "a", "1")]

        with self.assertRaises(InitializationException):
            optimizer = PlneOptimizer(start, finish, graph)
            optimizer.optimize()

    def test_no_path(self):
        start = "start"
        finish = "finish"
        graph = [(start, "a", "1"), ("b", finish, "1")]

        with self.assertRaises(OptimizationException):
            optimizer = PlneOptimizer(start, finish, graph)
            optimizer.optimize()

    def test_graph(self, n=100, p=0.3, min_weight=1.0, max_weight=10.0):
        start, finish, graph, G = generate_graph(
            n=n, p=p, min_weight=min_weight, max_weight=max_weight
        )

        objective, nodes = None, None
        length, path = None, None

        ex1, ex2 = None, None

        optimizer = PlneOptimizer(start, finish, graph)

        try:
            objective, _, nodes = optimizer.optimize()
        except OptimizationException as e:
            ex1 = e

        try:
            length, path = nx.single_source_dijkstra(G, start, target=finish)
        except nx.NetworkXNoPath as e:
            ex2 = e

        if ex1 is None and ex2 is None:
            self.assertAlmostEqual(objective, length)
            self.assertListEqual(nodes, path)
        elif ex1 is None:
            self.fail(f"A path was found only by Gurobi")
        elif ex2 is None:
            self.fail(f"A path was found only by Dijkstra")

    def test_small_graph(self):
        self.test_graph(n=10)

    def test_big_graph(self):
        self.test_graph(n=1000)

    def test_sparse_graph(self):
        self.test_graph(p=0.01)

    def test_dense_graph(self):
        self.test_graph(p=0.8)

    def test_complete_graph(self):
        self.test_graph(p=1)


if __name__ == "__main__":
    unittest.main()
