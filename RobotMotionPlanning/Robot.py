import numpy as np
import math
import random
from annoy import AnnoyIndex
from shapely.geometry import *
from Utils import *

class Environment:
    def __init__(self, width, height, robot):
        self.width = width
        self.height = height
        self.robot = robot
        self.obstacles = [ box(75, 75, 125, 125), box(275, 275, 325, 325 ), box(75, 275, 125, 325 ), box(275, 75, 325, 125 ), box(175, 125, 225, 175)]
        self.count = 0
        self.count2 = 0
    def collision_free(self, q): # tells if the robot hit one of the
        self.robot.update_angles(q)
        end_points = self.robot.get_end_points()

        robots_arms = []
        for i in range(len(end_points) - 1):
            p1 = end_points[i]
            p2 = end_points[i + 1]
            robots_arms.append(LineString([(p1.x, p1.y), (p2.x, p2.y)]))

        for robot_arm in robots_arms:
            for obstacle in self.obstacles:
                if obstacle.intersection(robot_arm):
                    return False
        return True

    def connects(self,q1, q2): # determines if two nodes should be connected by seeing if they have to
        # hit an obstacle to meet
        self.robot.update_angles(q1)
        end_points1 = self.robot.get_end_points()
        self.robot.update_angles(q2)
        end_points2 = self.robot.get_end_points()

        testLines = []
        # old angular distance hueristic
        # for i in range(len(q1)):
        #     if angular_distance(q1[i], q2[i]) > math.pi / 9:
        #         print("BOOM 2")
        #         return False
        #print(len(end_points1))
        #print(len(end_points2))
        for i in range(len(end_points1)): # iterates through the endpoints connects them with the next condfigs endpoints
            # to see if there is an obstacle in the way
            test_line = LineString([(end_points1[i].x,end_points1[i].y), (end_points2[i].x, end_points2[i].y)])
            testLines.append(test_line)
            self.count = + 1
            for obstacle in self.obstacles:
                if obstacle.intersection(test_line):
                    #print(end_points1)
                    #print("returning false")
                    self.count2 =+ 1
                    return False
        return True


class Point: # point class.. self explanitory
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def as_tuple(self):
        return (self.x, self.y)


class Robot: # robot class
    def __init__(self, fixed_x, fixed_y, arm_length, no_arms):
        self.fixed_x = fixed_x
        self.fixed_y = fixed_y
        self.arm_length = arm_length
        self.no_arms = no_arms
        self.angles = [math.pi / 4.0 for i in range(self.no_arms)]

    def update_angles(self, angles):
        self.angles = angles

    #def update_angles(self, rt):
    #   self.angles = [math.pi / rt for i in range(self.no_arms)]

    def get_random_angle(self): # generates a random angle
        return random.random() * 2 * math.pi

    def get_random_config(self): # get random config angles for the arms
        #return self.get_random_angle()
        return tuple([self.get_random_angle() for i in range(self.no_arms)])


    def euclidean_distance(self, p1, p2): # does what the name says
        return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    def distance(self, q1, q2): # gets the "distance" between two configs
        self.angles = q1
        q1_end_points = self.get_end_points()
        self.angles = q2
        q2_end_points = self.get_end_points()

        distances = [self.euclidean_distance(q1_end_points[i], q2_end_points[i]) for i in range(self.no_arms) ]

        return sum(distances) #/ float(len(distances))
        #return self.euclidean_distance(q1_end_points[-1], q2_end_points[-1])



    def get_end_points(self): # generates the endpoints from angles(based on the lecture kinematics)
        i = 0
        end_points = []
        x = self.fixed_x
        y = self.fixed_y
        new_point = Point(x, y)
        end_points.append(new_point)
        while i < len(self.angles):
            x = x + self.arm_length * np.cos(sum(self.angles[:i+1]))
            y = y + self.arm_length * np.sin(sum(self.angles[:i+1]))
            new_point = Point(x, y)
            end_points.append(new_point)
            i += 1

        return end_points

if __name__ == '__main__':

    ## testing to get the "connects" right
    ## was indexing wrong and not checking the last endpoint trajectory
    robot = Robot(200, 200, 75, 3)
    env = Environment(400, 400, robot)


    def draw():
        global G, node, x, path, env, robot

        clear()

        for obstacle in env.obstacles:
            draw_polygon(obstacle.exterior.coords)

        configs = [robot.get_random_config(), robot.get_random_config()]


        (result, testLines) = env.connects(configs[0], configs[1])
        print(result)
        print(len(testLines))

        for config in configs:
            robot.update_angles(config)
            end_points = robot.get_end_points()
            count = 0
            for i in range(len(end_points) - 1):
                set_fill_color(.00 + count, .00 + count, .00 + count)
                p1 = end_points[i]
                p2 = end_points[i + 1]
                draw_circle(p1.x, p1.y, 1)
                draw_polygon([(p1.x, p1.y), (p2.x, p2.y)])

                count += .2

        for testLine in testLines:
            set_stroke_color(1,0,0)
            draw_polygon(testLine.coords)
            set_stroke_color(0, 0, 0)

        sleep(1)



    start_graphics(draw, width=env.width, height=env.height)
