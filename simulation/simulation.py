import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import *
from grid.grid import Grid
from cell.cell import Cell
from erbast.erbast import Erbast
from carviz.carviz import Carviz
from vegetob.vegetob import Vegetob
from random import randint, random
from math import sqrt

class Simulation():
    def __init__(self):
        self.day = 0
        self.grid = Grid()

    def __str__(self):
        return f"Simulation: day:{self.day}, grid:{self.grid}"
    