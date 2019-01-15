from shapely.geometry import Polygon
from cs1lib import *



if __name__ == '__main__':
    polygons = [Polygon(((0, 0), (1, 0), (1, 1))), Polygon(((1, 1), (1, 0), (5, 1)))]

    def draw():
        clear()

        #set_fill_color(1,0,0)
        #draw_polygon([(0, 0), (1, 0), (1, 1)])
        #set_fill_color(0,1,0)
        #draw_polygon([(1, 1), (1, 0), (5, 1)])
        #print(polygons[0].overlaps(polygons[1]))

    start_graphics(draw, 500, 500)