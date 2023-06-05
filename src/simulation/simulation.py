import os
import copy
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from constants import *
from src.grid.grid import Grid
from src.cell.cell import Cell
from src.erbast.erbast import Erbast
from src.carviz.carviz import Carviz
from src.vegetob.vegetob import Vegetob
from math import sqrt

class Simulation():
    def __init__(self):
        self.day = 0
        self.grid = Grid()
        self.gridStatuses = []

    def __str__(self):
        return f"Simulation: day:{self.day}, grid:{self.grid}"
    
    def giveSomeCellsWater(self):
        for row in self.grid.cells:
            for cell in row:
                if cell.type == "ground" and random.random() < WATER_CHANCE:
                    cell.type = "water"

    

    def growing(self):
        new_grid = []
        for row in self.grid.cells:
            new_row = []
            for cell in row:
                if cell.type == "ground":
                    cell.vegetob.density += GROWING
                    if cell.vegetob.density > 100:
                        cell.vegetob.density = 100
                new_row.append(cell)
            new_grid.append(new_row)
        self.grid.cells = copy.deepcopy(new_grid)

    def move(self):
        updated_cells = []
        for row in self.grid.cells:
            updated_row = []
            for cell in row:
                if cell.type == "ground":
                    # Form herds and prides
                    herds = cell.herds
                    prides = cell.prides
                    herdToMove = []
                    prideToMove = []
                    # Evaluate the most appealing cell in the neighborhood
                    neighbors = self.grid.getNeighbors(cell.x, cell.y)
                    bestCell = None
                    bestCellValue = -1
                    for neighbor in neighbors:
                        if neighbor.vegetob != 0:
                            if neighbor.vegetob.density > bestCellValue:
                                bestCell = neighbor
                                bestCellValue = neighbor.vegetob.density
                    for herd in herds:
                        for erbast in herd:
                            if erbast.energy > 0:
                                if erbast.hasMoved:
                                    continue
                                else:
                                    # Individual decision-making
                                    if erbast.energy < THRESHOLD_E:  # Individual with low energy stays and can graze
                                        self.graze(erbast, cell)
                                        erbast.hasMoved = False
                                        continue
                                    elif bestCellValue > cell.vegetob.density:  # Herd moves to the best cell
                                        if erbast.socialAttitude >= random.random():  # Individual follows the herd's decision
                                            herdToMove.append(erbast)
                                            herd.remove(erbast)
                                            erbast.hasMoved = True
                                            erbast.energy -= 1
                                            if erbast.energy < 0:
                                                herd.remove(erbast)
                                            continue
                                    # Individual decision to stay
                                    erbast.hasMoved = True
                                    erbast.energy -= 1
                                    if erbast.energy < 0:
                                        herd.remove(erbast)
                                        herdToMove.remove(erbast)
                                    continue
                    for pride in prides: 
                        for carviz in pride:
                            if carviz.energy > 0:
                                if carviz.hasMoved:
                                    continue
                                else:
                                    # Individual decision-making
                                    if carviz.energy < THRESHOLD_C:
                                        carviz.hasMoved = False
                                        continue
                                    elif bestCellValue > cell.vegetob.density: 
                                        if carviz.socialAttitude >= random.random():
                                            prideToMove.append(carviz)
                                            pride.remove(carviz)
                                            carviz.hasMoved = True
                                            carviz.energy -= 1
                                            if carviz.energy < 0:
                                                pride.remove(carviz)
                                            continue
                                    carviz.hasMoved = True
                                    carviz.energy -= 1
                                    if carviz.energy < 0:
                                        pride.remove(carviz)
                                        prideToMove.remove(carviz)
                                    continue

                    bestCell.herds.extend(herdToMove)
                    bestCell.prides.extend(prideToMove)
                
                updated_row.append(cell) 
            updated_cells.append(updated_row)  
        self.grid.cells = copy.deepcopy(updated_cells) 


    def graze(self, erbast, cell):
        if isinstance(cell, Cell) and isinstance(cell.vegetob, Vegetob):  # Check if cell and vegetob exist
            if cell.vegetob.density > 0:
                erbast.energy += 1
                cell.vegetob.density -= 1
                if cell.vegetob.density < 0:
                    cell.vegetob.density = 0
        else:
            erbast.socialAttitude -= 0.1
            if erbast.socialAttitude < 0:
                erbast.socialAttitude = 0

    def grazing(self):
        for row in self.grid.cells:
            for cell in row:
                if cell.type == "ground":
                    for herd in cell.herds:
                        for erbast in herd:
                            if not erbast.hasMoved:
                                self.graze(erbast, cell)
                                cell.herds.remove(herd)
                                cell.herds.append(herd)
        

    def reorganize_social_groups(self):
        for row in self.grid.cells:
            for cell in row:
                if len(cell.herds) > 1:
                    merged_herd = []
                    for herd in cell.herds:
                        merged_herd.extend(herd)
                    cell.herds = [merged_herd]

                if len(cell.prides) > 1:
                    if sum(carviz.socialAttitude for carviz in cell.prides[0]) < 10 or sum(carviz.socialAttitude for carviz in cell.prides[1]) < 10:
                        winningPride = self.fight_between_prides(cell.prides[0], cell.prides[1])
                        cell.prides = [winningPride]
                    else:
                        merged_pride = []
                        for pride in cell.prides:
                            merged_pride.extend(pride)
                        cell.prides = [merged_pride]

    def increase_social_attitude(self, pride):
        for carviz in pride:
            carviz.socialAttitude += 0.1
            if carviz.socialAttitude > 1:
                carviz.socialAttitude = 1

    def decrease_social_attitude(self, pride):
        for carviz in pride:
            carviz.socialAttitude -= 0.1
            if carviz.socialAttitude < 0:
                carviz.socialAttitude = 0

    def fight_between_prides(self, pride1, pride2):
        total_energy_pride1 = sum(carviz.energy for carviz in pride1)
        total_energy_pride2 = sum(carviz.energy for carviz in pride2)
        total_energy = total_energy_pride1 + total_energy_pride2

        rand_num = random.random()  # Draw a random number
        probability_pride1 = total_energy_pride1 / total_energy
        if rand_num <= probability_pride1:
            self.increase_social_attitude(pride1)  
            self.decrease_social_attitude(pride2)  
            return pride1
        else:
            # Pride 2 wins
            self.increase_social_attitude(pride2)  
            self.decrease_social_attitude(pride1)  
            return pride2
        
    def hunt_by_pride(self, pride, erbast):
        total_energy_pride = sum(carviz.energy for carviz in pride)
        rand_num = random.random() 
        probability_success = total_energy_pride / (total_energy_pride + erbast.energy)

        if rand_num <= probability_success:
            prey_energy = erbast.energy
            prey_energy_share = prey_energy // len(pride)
            spare_energy = prey_energy % len(pride)  

            for carviz in pride:
                carviz.energy += prey_energy_share
            lowest_energy_carviz = min(pride, key=lambda x: x.energy)
            lowest_energy_carviz.energy += spare_energy

            self.increase_social_attitude(pride) 
        else:
            self.decrease_social_attitude(pride) 

    def chooseStrongestErbast(self, herd):
        strongestErbast = None
        strongestErbastEnergy = -1
        for erbast in herd:
            if erbast.energy > strongestErbastEnergy:
                strongestErbast = erbast
                strongestErbastEnergy = erbast.energy
        return strongestErbast  
    
    def struggle(self):
        for row in self.grid.cells:
            for cell in row:
                self.reorganize_social_groups()

                if len(cell.prides) > 1:
                    self.fight_between_prides(cell.prides[0], cell.prides[1])
                elif (len(cell.prides) == 1) and (len(cell.herds) == 1):
                    strongestErbast = self.chooseStrongestErbast(cell.herds[0])
                    self.hunt_by_pride(cell.prides[0], strongestErbast)
                else:
                    continue

    
    def spawning(self):
        for row in self.grid.cells:
            for cell in row:
                for herd in cell.herds:
                    for erbast in range(len(herd)):
                        herd[erbast].age += 1
                        if herd[erbast].age % 10 == 0:
                            herd[erbast].energy -= AGING
                        if herd[erbast].age >= herd[erbast].lifetime:
                            if len(cell.herds[0]) < MAX_HERD or MAX_HERD is None:
                                offspring_energy = herd[erbast].energy

                                for _ in range(2):
                                    offspring_age = 0
                                    offspring_energy_share = offspring_energy // 2
                                    offspring_lifetime = 2 * herd[erbast].lifetime if herd[erbast].lifetime <= MAX_LIFE_E // 2 else MAX_LIFE_E
                                    offspring_social_attitude = 2 * herd[erbast].socialAttitude if herd[erbast].socialAttitude <= 0.5 else 1
                                    offspring = Erbast(offspring_energy_share, offspring_lifetime, offspring_age, offspring_social_attitude)
                                    cell.herds[0].append(offspring)

                for pride in cell.prides:
                    for carviz in range(len(pride)):
                        pride[carviz].age += 1
                        if pride[carviz].age % 10 == 0:
                            pride[carviz].energy -= AGING
                        if pride[carviz].age >= pride[carviz].lifetime:
                            if len(cell.prides[0]) < MAX_PRIDE or MAX_PRIDE is None:
                                offspring_energy = pride[carviz].energy

                                for _ in range(2):
                                    offspring_age = 0
                                    offspring_energy_share = offspring_energy // 2
                                    offspring_lifetime = 2 * pride[carviz].lifetime if pride[carviz].lifetime <= MAX_LIFE_C // 2 else MAX_LIFE_C
                                    offspring_social_attitude = 2 * pride[carviz].socialAttitude if pride[carviz].socialAttitude <= 0.5 else 1
                                    offspring = Carviz(offspring_energy_share, offspring_lifetime, offspring_age, offspring_social_attitude)
                                    cell.prides[0].append(offspring)

    def populateMapWithErbastAndCarviz(self, erbast_prob, carviz_prob):
        for row in self.grid.cells:
            for cell in row:
                if cell.type == "ground":
                    # Populate with Erbast
                    for _ in range(MAX_HERD):
                        if random.random() <= erbast_prob:
                            age = 0
                            energy = MAX_ENERGY_E
                            social_attitude = random.random()
                            lifetime = random.randint(0, MAX_LIFE_E)
                            erbast = Erbast(energy, lifetime, age, social_attitude)
                            cell.herds.append([erbast])

                    for _ in range(MAX_PRIDE):
                        if random.random() <= carviz_prob:
                            age = 0
                            energy = MAX_ENERGY_C
                            lifetime = random.randint(0, MAX_LIFE_C)
                            social_attitude = random.random()
                            carviz = Carviz(energy, lifetime, age, social_attitude)
                            cell.prides.append([carviz])

    


    def start(self):
        self.giveSomeCellsWater()
        self.populateMapWithErbastAndCarviz(0.1, 0.9)
        self.gridStatuses = [self.grid]
        changes = []
        for day in range(NUMDAYS):
            print(f"Day {day}")
            self.growing()
            print("Growing done")
            self.move()
            print("Move done")
            self.grazing()
            print("Grazing done")
            self.struggle()
            print("Struggle done")
            self.spawning()
            print("Spawning done")
            self.day += 1
            changes.append(self.grid.cells.copy())
            self.gridStatuses.append(copy.deepcopy(self.grid))
            
        print(self.gridStatuses)

        self.plot_terrain()
        self.vegetobDensityPlot()
        self.plotAverageCarvizErbastPopulation()
        self.plotPopulationScatter()

    def plot_terrain(self):
        grid = self.grid
        
        fig, ax = plt.subplots()
        
        for row in grid.cells:
            for cell in row:
                x = cell.x
                y = cell.y

                if cell.type == "ground":
                    color = "brown"
                else:
                    color = "blue"

                rect = plt.Rectangle((x, y), 1, 1, facecolor=color)
                ax.add_patch(rect)

        ax.set_xlim(0, len(grid.cells))
        ax.set_ylim(0, len(grid.cells[0]))
        ax.set_aspect('equal')
        ax.set_title("Terrain Disposition between Water and Ground")
        ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, facecolor='blue'), plt.Rectangle((0, 0), 1, 1, facecolor='brown')],
              labels=['Water', 'Ground'], loc='upper right')
        ax.set_xticks(range(len(grid.cells) + 1))
        ax.set_yticks(range(len(grid.cells[0])+ 1))
        ax.grid(True)
        
        plt.tight_layout()
        plt.show()

    def vegetobDensityPlot(self):
        gridStatuses = self.gridStatuses
        fig, ax = plt.subplots(figsize=(6, 6))
        cmap = plt.cm.get_cmap('Greens')
        density_grid = np.zeros((len(gridStatuses[0].cells), len(gridStatuses[0].cells[0])), dtype=float)
        im = ax.imshow(density_grid, cmap=cmap, vmin=0, vmax=100)
        ax.set_title('Vegetob Density Map')
        ax.axis('off')
        cbar = fig.colorbar(im)
        cbar.set_label('Density')

        def update(frame):
            nonlocal density_grid
            for i in range(len(gridStatuses[frame].cells)):
                for j in range(len(gridStatuses[frame].cells[i])):
                    cell = gridStatuses[frame].cells[i][j]
                    if isinstance(cell, Cell) and isinstance(cell.vegetob, Vegetob):
                        density_grid[i, j] = cell.vegetob.density
                    else:
                        density_grid[i, j] = 0
            im.set_array(density_grid)
            ax.set_title(f'Vegetob Density Map (Day {frame})')

        def init():
            im.set_array(density_grid)
            return im,

        anim = FuncAnimation(fig, update, frames=len(gridStatuses), init_func=init, interval=500, repeat=False)
        plt.show()

    def plotAverageCarvizErbastPopulation(self):
        gridStatuses = self.gridStatuses
        days = range(len(gridStatuses))
        erbast = []
        carviz = []
        
        for grid in gridStatuses:
            erbast_count = 0
            carviz_count = 0
            
            for row in grid.cells:
                for cell in row:
                    if cell.type == "ground":
                        for herd in cell.herds:
                            erbast_count += len(herd)
                        for pride in cell.prides:
                            carviz_count += len(pride)
            
            erbast.append(erbast_count)
            carviz.append(carviz_count)
        
        fig, ax = plt.subplots()
        ax.plot(days, erbast, label='Erbast')
        ax.plot(days, carviz, label='Carviz')

        ax.set(xlabel='Days', ylabel='Population',
            title='Population over time')
        ax.grid()
        ax.legend()

        plt.show()
    
    def plotPopulationScatter(self):
        gridStatuses = self.gridStatuses
        days = range(len(gridStatuses))
        erbast_total_population = []
        carviz_total_population = []

        for grid in gridStatuses:
            erbast_population = 0
            carviz_population = 0

            for row in grid.cells:
                for cell in row:
                    if cell.type == "ground":
                        erbast_population += sum(len(herd) for herd in cell.herds)
                        carviz_population += sum(len(pride) for pride in cell.prides)
            
            erbast_total_population.append(erbast_population)
            carviz_total_population.append(carviz_population)
        
        print(erbast_total_population)
        print(carviz_total_population)
        fig, ax = plt.subplots()
        ax.scatter(days, erbast_total_population, c='green', label='Erbast')
        ax.scatter(days, carviz_total_population, c='red', label='Carviz')

        ax.set(xlabel='Days', ylabel='Total Population',
            title='Total Population Scatter Plot')
        ax.grid()
        ax.legend()

        plt.show()
