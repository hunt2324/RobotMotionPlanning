import networkx as nx
from Robot import *
from cs1lib import *
from random import choice
from time import *
from Utils import *
from shapely.geometry import *
from math import *
from astar_search import *

class RRTNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class RRTGraph:

    def __init__(self):
        self.graph = {}
        self.number_of_edges = 0
        self.number_of_nodes = 0
        self.goal_state = 0
        self.start_state = 0

    def nodes(self):
        return self.graph.keys()

    def __str__(self):
        string = "PRM problem "
        return string

    def add_node(self, value):
        node = value
        if self.graph.get(node) == None:
            self.graph[node] = []
            self.number_of_nodes += 1
            #print(node)
            return True
        return False


    def add_edge(self, node1, node2):
        adjacenct_nodes1 = self.graph.get(node1)
        adjacenct_nodes2 = self.graph.get(node2)
        #print(adjacenct_nodes1)
        if self.graph.get(node1) == None:
            self.add_node(node1)

        if self.graph.get(node2) == None:
            self.add_node(node2)

        if adjacenct_nodes1 == None:
            adjacenct_nodes1 = []

        if adjacenct_nodes2 == None:
            adjacenct_nodes2 = []

        if node2 in adjacenct_nodes1:
            return False

        if node1 in adjacenct_nodes2:
            return False
        adjacenct_nodes1.append(node2)
        adjacenct_nodes2.append(node1)
        self.graph[node1] = adjacenct_nodes1
        self.graph[node2] = adjacenct_nodes2
        self.number_of_edges += 1
        return True

    def hueristic_fn(self, node):
        x_dist = abs(node[0] - self.goal_state[0])
        y_dist = abs(node[1] - self.goal_state[1])
        x_squared = x_dist ** 2
        y_squared = y_dist ** 2
        #print(sqrt(y_squared + x_squared))
        ## print(sqrt(y_squared + x_squared))
        return sqrt(y_squared + x_squared)

    def get_successors(self, node):
        successors = self.graph.get(node)
        #print(successors[0])
        return successors

    def is_goal(self, node):
        return self.goal_state == node

    def shortest_path(self, graph, intial, goal):
        self.goal_state = goal
        self.start_state = intial
        solution = astar_search(graph, self.hueristic_fn)
        #print(str(solution.path) + "hello123")
        return solution.path

    def connects(self, q1, q2):
        return True


if __name__ == '__main__':

    graph = RRTGraph()
    node = 1
    graph.add_node(node)
    node2 = 2
    graph.add_node(node2)
    graph.add_edge(node,node2)
    graph.get_successors(node)
    #print(graph.shortest_path(graph,node, node2 ))
