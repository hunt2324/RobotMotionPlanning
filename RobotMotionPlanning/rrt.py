# using shapely for collision detection
from time import *
from shapely.geometry import Polygon, Point
import networkx as nx
from Robot import *
from cs1lib import *
from random import *
from time import *
from Utils import *
from shapely.geometry import *
from PRMGraph import *
from RRTGraph import *
from math import *
from planarsim import *

poly = Polygon(((0, 0), (0, 1), (1, 1), (1, 0)))
point = Point(2, .2)

#print(poly)
#print(poly.contains(point))
controls_rs = array([
            [1, 0, 0],
            [-1, 0, 0],
            [1, 0, -1],
            [1, 0, 1],
            [-1, 0, -1],
            [-1, 0, 1]])

def k_closest_neighbors(G, k, q, distance): # same k_closest as PRM
    distances_dict = {}
    for q2 in G.nodes():
        d = distance(q, q2)
        distances_dict[d] = q2
    distances = list(distances_dict.keys())
    distances.sort()
    if distances[0] == 0.0:
        distances.pop(0)
    ordered_config = []
    for d in distances[0:k]:
        ordered_config.append(distances_dict[d])
    return ordered_config

def random_loc(width, height): # pick a random location on the display
    x = random.randint(0, width)
    y = random.randint(0, height)
    return(x,y)

def euclidean_distance(node1, node2): # calculate the distance between two points
    x_dist = abs(node1[0] - node2[0])
    y_dist = abs(node1[1] - node2[1])
    x_squared = x_dist ** 2
    y_squared = y_dist ** 2
    return sqrt(y_squared + x_squared)

def create_config(node, duration, width, height): # creates a new congig from the random point given
    test = False
    count = 0
    while test == False: # while its not outside grid
        count += 1
        control_index = random.randint(0,5)
        control = controls_rs[control_index]
        old_state = transform_from_config(node)
        pre_convert = single_action(old_state, control, duration)
        new_config = config_from_transform(pre_convert)
        x = new_config[0]
        y = new_config[1]
        theta = new_config[2]
        if x < 0 or x > width or y < 0 or y > height: # if its outside the grid do the loop again
            test = False
            continue
        else: # else dont do it again
            test = True
        new_config = (x, y, theta)
        return new_config


def nearest_node(q, G): # find the nearest node(in the graph) to the random chosen spot on the grid
    d = float("inf")
    for node in G.nodes():
        node_dist = euclidean_distance(node, q)
        if node_dist < d:
            new_node = node
            d = node_dist

    q = new_node
    return q


def hueristic_fn2(self, node, node2):
    x_dist = abs(node[0] - node2[0])
    y_dist = abs(node[1] - node2[1])
    x_squared = x_dist ** 2
    y_squared = y_dist ** 2
    #print(sqrt(y_squared + x_squared))
    print(sqrt(y_squared + x_squared))
    return sqrt(y_squared + x_squared)
def RRT(qintial, k , duration, width, height):
    G =RRTGraph()
    G.add_node(qintial)

    for i in range(k):
        q_rand = random_loc(width, height)
        q_near = nearest_node(q_rand, G)
        #print(q_near)
        node_to_add = create_config(q_near, duration, width, height)
        G.add_node(node_to_add)
        G.add_edge(q_near, node_to_add)
    return G
def Query(q_init, q_goal, k, G, distance, connects):
    #print("got here1234\n")
    N_q_init = k_closest_neighbors(G, k, q_init, distance)
    N_q_goal = k_closest_neighbors(G, k, q_goal, distance)

    G.add_node(q_init)
    G.add_node(q_goal)

    for q_prime in N_q_init:
        if connects(q_init, q_prime):
            G.add_edge(q_init, q_prime)
            break

    for q_prime in N_q_goal:
        if connects(q_goal, q_prime):
            G.add_edge(q_goal, q_prime)
            break
    #print(nx.shortest_path(G, q_init, q_goal))
    #print("got here\n")
    return G.shortest_path(G, q_init, q_goal) # uses a* to find the shortest path

def connects(self,q1, q2):
    return True


if __name__ == '__main__':
    G = RRT((100, 100, pi), 10000, 15, 800, 800)
    G.goal_state = (200,200,pi)
    path = Query((100, 100, pi), (700,700, pi), 15, G,  euclidean_distance, G.connects)
    print(path)
    count = 0
    def draw(): # draws the robot as a red circle transversing the graph built by RRT
        global count
        clear()
        set_fill_color(0,0,0)
        set_stroke_color(0,0,0)
        if count == len(path):
            print("Done")
            count = 0
            print("Restart")
            return

        for node in G.nodes():
            a_list = G.graph.get(node)
            for i in a_list:
                line = LineString([i,node])
                draw_polygon([i,node])
        set_fill_color(1,0,0)
        set_stroke_color(1,0,0)
        draw_circle(path[count][0], path[count][1],10)
        count += 1
        sleep(.2)

    start_graphics(draw, width=800, height=800)
