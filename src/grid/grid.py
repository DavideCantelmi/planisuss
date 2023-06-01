import os
import sys 

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.cell.cell import Cell
from constants import *

class Grid():
    def __init__(self):
        self.cells = []
        for i in range(NUMCELLS):
            row = []
            for j in range(NUMCELLS):
                if i == 0 or i == NUMCELLS-1 or j == 0 or j == NUMCELLS-1:
                    row.append(Cell(i,j,"water"))
                else:
                    row.append(Cell(i,j,"ground"))
            self.cells.append(row)
        
        for i in range(NUMCELLS):
            for j in range(NUMCELLS):
                print(self.cells[i][j])
    
    def __str__(self):
        return f"Grid: cells:{list(self.cells)}"
    
    def getCell(self, x, y):
        for cell in self.cells:
            if cell.x == x and cell.y == y:
                return cell
        return None
    
    def getNeighbors(self, x, y):
        if x < 0 or x > NUMCELLS-1 or y < 0 or y > NUMCELLS-1:
            raise ValueError("x and y must be between 0 and NUMCELLS-1")
        neighbors = []
        for row in self.cells:
            for cell in row:
                if (abs(cell.x - x) <= 1) and (abs(cell.y - y) <= 1):
                    neighbors.append(cell)
        return neighbors