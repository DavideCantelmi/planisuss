"""
The time on Planisuss is structured in units called day. A day is articulated in the following phases:
Growing Vegetob grow everywhere of a fixed quantity (GROWING).
Movement The individuals of animal species (Erbast and Carviz) decide if move in another
area. Movement is articulated as individual and social group (herd or pride) movement. Grazing Erbast which did not move, 
can graze the Vegetob in the area.
Struggle Carviz insisting on the same area can fight or hunt.
Spawning Individuals of animal species can generate their offspring.
Conventionally, long periods of time on Planisuss are measured in months, years, decades and centuries, 
where a month is 10 days long, a year is 10 months long, a decade is 10 years long, and a century is 10 decades long.
"""



import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from constants import *
from src.grid.grid import Grid
from src.cell.cell import Cell
from src.erbast.erbast import Erbast
from src.carviz.carviz import Carviz
from src.vegetob.vegetob import Vegetob
from random import randint, random
from math import sqrt

class Simulation():
    def __init__(self):
        self.day = 0
        self.grid = Grid()

    def __str__(self):
        return f"Simulation: day:{self.day}, grid:{self.grid}"
    
    def giveSomeCellsWater(self):
        for cell in self.grid.cells:
            if cell.type == "ground" and random() < WATER_CHANCE:
                cell.type = "water"

    
    """
    The Vegetob density is increased by GROWING. If a cell is completely surrounded by cells having the maximum Vegetob density, 
    the animals present in the cell are overwhelmed by the Vegetob and terminated.
    """

    def growing(self):
        for cell in self.grid.cells:
            if cell.type == "ground":
                cell.vegetob.density += GROWING
                if cell.vegetob > 100:
                    cell.vegetob.density = 100
            else:
                cell.vegetob = 0

    """
    In the Movement phase, individuals and social groups evaluate the possibility to move in another cell. Based on suitable rules, the most appealing cell in the neighborhood is identified. The evaluation is carried on first by social group basis (herd and pride).
    All the Erbast in a cell at the beginning of the day form a herd. Similarly, all the Carviz 
    in a cell constitute a pride. Social groups can have memories and strategies: 
    proper values can be stored and used in the evaluation and planning. 
    For instance, they can be provided with the coordinate of the last cell visited to avoid to move back, or the density of nutrients of cells visible in previous days.
    Once the herd and the pride of the cell made a decision (stay or move), the individuals can choose if they will follow the social group or made a different decision, splitting by the social group.
    Splitting decision can be formed considering the properties of the individual (e.g., the herd will move, while the individual having a low value of energy may stay; or, on the contrary,
    the herd will stay, but strong Erbast may want to move, due to the lack of Vegetob in the cell) 
    and is weighted with the social attitude of the individual.
    Movements take place for all the cells at the same time and are instantaneous. 
    The movement costs to each individual one point of Energy.
    Not everyone moves: the individuals that do not move can graze the Vegetob in the cell.
    """
    def move(self):
        for cell in self.grid.cells:
            if cell.type == "ground":
                if len(cell.herd) > 0:
                    for erbast in cell.herd:
                        if erbast.energy > 0:
                            if erbast.hasMoved:
                                continue
                            else:
                                # evaluate the most appealing cell in the neighborhood
                                neighbors = self.grid.getNeighbors(cell.x, cell.y)
                                bestCell = None
                                bestCellValue = -1
                                for neighbor in neighbors:
                                    if neighbor.vegetob.density > bestCellValue:
                                        bestCell = neighbor
                                        bestCellValue = neighbor.vegetob.density
                                if bestCellValue > cell.vegetob.density:
                                    # move
                                    bestCell.herd.append(erbast)
                                    cell.herd.remove(erbast)
                                    erbast.hasMoved = True
                                    erbast.energy -= 1
                                    if erbast.energy < 0:
                                        cell.herd.remove(erbast)
                                    continue
                                else:
                                    # stay
                                    erbast.hasMoved = True
                                    erbast.energy -= 1
                                    if erbast.energy < 0:
                                        cell.herd.remove(erbast)
                                    continue
                if len(cell.pride) > 0:
                    for carviz in cell.pride:
                        if carviz.energy > 0:
                            if carviz.hasMoved:
                                continue
                            else:
                                # evaluate the most appealing cell in the neighborhood
                                neighbors = self.grid.getNeighbors(cell.x, cell.y)
                                bestCell = None
                                bestCellValue = -1
                                for neighbor in neighbors:
                                    if neighbor.vegetob.density > bestCellValue:
                                        bestCell = neighbor
                                        bestCellValue = neighbor.vegetob.density
                                if bestCellValue > cell.vegetob.density:
                                    # move
                                    bestCell.pride.append(carviz)
                                    cell.pride.remove(carviz)
                                    carviz.hasMoved = True
                                    carviz.energy -= 1
                                    if carviz.energy < 0:
                                        cell.pride.remove(carviz)
                                    continue
                                else:
                                    # stay
                                    carviz.hasMoved = True
                                    carviz.energy -= 1
                                    if carviz.energy < 0:
                                        cell.pride.remove(carviz)
                                    continue
            else:
                continue
    
    """
    The Erbast that did not move, can graze to increment their Energy. The grazing decreases the Vegetob density of the cell. 
    Every Erbast can have 1 point of Energy for 1 point of Vegetob density. 
    If the Vegetob density is lower than the number of Erbast, 1 point is assigned to those Erbast having the lowest value of Energy, 
    up to exhaustion of the Vegetob of the cell.
    Optionally, the Social attitude of those individuals that did not eat (due to lack of Vegetob) can be decreased.
    """

    def grazing(self):
        for cell in self.grid.cells:
            if cell.type == "ground":
                if len(cell.herd) > 0:
                    for erbast in cell.herd:
                        if erbast.energy > 0 and not erbast.hasMoved:
                            if cell.vegetob.density > 0:
                                erbast.energy += 1
                                cell.vegetob.density -= 1
                            else:
                                erbast.energy -= 1
                                if erbast.energy < 0:
                                    cell.herd.remove(erbast)