
import networkx as nx
from Robot import *
from cs1lib import *
from random import choice
from time import *


def angular_distance(a1, a2):
    _2pi = math.pi * 2
    _p = abs(a1-a2) % _2pi
    return _2pi - _p if _p > math.pi else _p

if __name__ == '__main__':

    print(angular_distance(math.pi*2 - math.pi/4, 0))
