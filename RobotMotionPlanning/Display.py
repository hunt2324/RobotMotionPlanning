from cs1lib import *
from Robot import *

rt = 4

if __name__ == '__main__':

    env = Environment(500, 500)
    robot = Robot(250, 250, 50, 3)


    def draw():
        global rt
        rt += 1
        robot.update_angles(rt)
        end_points = robot.get_end_points()
        count = 0
        for i in range(len(end_points)-1):
            set_fill_color(.00 + count, .00 + count, .00 + count)
            #set_fill_color(0.1, 0.8, 0.1)
            p1 = end_points[i]
            p2 = end_points[i+1]
            draw_circle(p1.x, p1.y, 5)
            draw_polygon([(p1.x, p1.y),  (p2.x, p2.y)])

            count += .2

    start_graphics(draw, width=env.width, height=env.height)