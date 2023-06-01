"""
Planisuss is regularly structured in geographical units called cells. Cells are organized in a regular grid structure and their position can be identified by a bidimensional coordinate.
The size of Planisuss is NUMCELLS × NUMCELLS cells.
The cells can be occupied by water or ground. Cells on the boundary of the grid are always occupied by water. All the other cells are suitably assigned either to water or ground at the beginning of the simulation.
Each ground cell can host individuals of the three species, while water cells are uninhabitable. A suitable procedure initializes the content of the cells at the beginning of the simulation.
All the Erbast in a cell constitute a herd. Similarly, all the Carviz in a cell constitute a pride. The basic events on Planisusshappen in discrete time units called days. For practical purposes,
the simulation can be terminated after a predefined number of days, NUMDAYS.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from constants import *
from src.vegetob.vegetob import Vegetob

types = ["water","ground"]

class Cell:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.vegetob = Vegetob(0)
        self.herds = []
        self.prides = []

    def __str__(self):
        return f"Cell: x:{self.x}, y:{self.y}, type:{self.type}, vegetob:{self.vegetob}, herds:{self.herds}, prides:{self.prides}"