
import networkx as nx
from Robot import *
from cs1lib import *
from random import choice
from time import *
from Utils import *
from shapely.geometry import *
from PRMGraph import *

def k_closest_neighbors(G, k, q, distance):
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


# http://www.cs.columbia.edu/~allen/F15/NOTES/Probabilisticpath.pdf
# note to self for psuedo code ^^^
def PRM(n, k, random_config, collision_free, distance, connects):
    #G = nx.Graph() # old code when i thought we could use a graph module
    G = PrmGraph()


    while G.number_of_nodes < n:
        q = random_config()
        while not collision_free(q):
            q = random_config()
        G.add_node(q)

    for q in G.nodes():
        k_closest = k_closest_neighbors(G, k, q, distance)
        for configuration in k_closest:
            if connects(q, configuration): # checks if the config connects quote unquote
                G.add_edge(q, configuration) # adds edge if it connects

    print(G.number_of_nodes)
    print(G.number_of_edges)
    return G


def Query(q_init, q_goal, k, G, distance, connects):
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
    return G.shortest_path(G, q_init, q_goal) # use a* to calc the end




def angular_distance_arms(q1, q2):
    return sum([angular_distance(q1[i], q2[i]) for i in range(len(q1))])

#def hueristic_fn(self, node):
 #       return sum([angular_distance(node.value[i], q2[i]) for i in range(len(q1))])

if __name__ == '__main__':

    robot = Robot(200, 200, 50, 4)
    env = Environment(400, 400, robot)


    G = PRM(6000, 10, robot.get_random_config, env.collision_free, angular_distance_arms, env.connects)
    path = Query((math.pi, 0, 0, 0), (0, 0, 0, 0), 5, G, angular_distance_arms, env.connects)
    node = None
    if len(path) == 0:
        print("No path found")
    else:
        node = path[0]
    x = 0

    def draw(): # draws pretty much everything
        global G, node, x, path, env
        enable_smoothing() # attempting to do some unrealistic antialiasing lol

        clear()
        enable_smoothing()

        for obstacle in env.obstacles: # draw obstacles
            draw_polygon(obstacle.exterior.coords)

        if node is not None:
            robot.update_angles(node)
            end_points = robot.get_end_points()
            count = 0
            for i in range(len(end_points) - 1):
                set_fill_color(.00 + count, .00 + count, .00 + count) # not used but fragile(I know not great code here)
                p1 = end_points[i]
                p2 = end_points[i + 1]
                draw_circle(p1.x, p1.y, 1)
                draw_polygon([(p1.x, p1.y), (p2.x, p2.y)])

                count += .2
        sleep(.2)
        x += 1
        if x < len(path):
            node = path[x]
        elif len(path) == 0:
            node = None
        else:
            node = path[0] # start drawing process over so i can actually know what's going on
            x = 0


    start_graphics(draw, width=env.width, height=env.height)