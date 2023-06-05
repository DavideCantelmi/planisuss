import os
import copy
import sys
import numpy as np
import matplotlib.pyplot as plt
import collections.abc as abc
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
                        if herd is not None and hasattr(herd, "__iter__"):
                            for erbast in herd:
                                if erbast.energy > 0:
                                    if erbast.hasMoved and erbast.energy > THRESHOLD_E:
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
                                                erbast.energy -= 10
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
                            if carviz is None or not hasattr(carviz, "socialAttitude"):
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
        if isinstance(cell, Cell) and isinstance(cell.vegetob, Vegetob): 
            if cell.vegetob.density > 0:
                erbast.energy += 1
                print(f"Erbast grazed in cell {cell.x}, {cell.y}")
                cell.vegetob.density -= 10
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
                    if len(cell.herds) or not cell.herds == 0:
                        continue
                    else:
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
                        if herd is not None and hasattr(herd, "__iter__"):
                         merged_herd.extend(herd)
                    cell.herds = [merged_herd] if merged_herd else []

                if len(cell.prides) > 1:
                    if any(carviz is None or not hasattr(carviz, "socialAttitude") for carviz in cell.prides[0]) or any(carviz is None or not hasattr(carviz, "socialAttitude") for carviz in cell.prides[1]):
                        winningPride = self.fight_between_prides(cell.prides[0], cell.prides[1])
                        cell.prides = [winningPride] if winningPride else []
                    else:
                        merged_pride = []
                        for pride in cell.prides:
                            if pride:
                                merged_pride.extend(pride)
                        cell.prides = [merged_pride] if merged_pride else []

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
        if erbast is not None and hasattr(erbast, "energy"):
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
        if herd is None or not hasattr(herd, "__iter__"):
            strongestErbast = None
            strongestErbastEnergy = -1
            if herd is not None and hasattr(herd, "__iter__"):
                for erbast in herd:
                    if erbast.energy > strongestErbastEnergy:
                        strongestErbast = erbast
                        strongestErbastEnergy = erbast.energy
                return strongestErbast  
        else: 
            pass
    
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
                if cell.herds is not None and hasattr(cell.herds, "__iter__"):
                    for herd in cell.herds:
                        if herd is not None and hasattr(herd, "__iter__"):
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
                                            if offspring_energy_share <= 0:
                                                break
                                            offspring_lifetime = 2 * herd[erbast].lifetime if herd[erbast].lifetime <= MAX_LIFE_E // 2 else MAX_LIFE_E
                                            offspring_social_attitude = 2 * herd[erbast].socialAttitude if herd[erbast].socialAttitude <= 0.5 else 1
                                            offspring = Erbast(offspring_energy_share, offspring_lifetime, offspring_age, offspring_social_attitude)
                                            cell.herds[0].append(offspring)
                if cell.prides is not None and hasattr(cell.prides, "__iter__"):
                    for pride in cell.prides:
                        if pride is not None and hasattr(pride, "__iter__"):
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
                                            if offspring_energy_share <= 0:
                                                break
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
                            if herd is not None and hasattr(herd, "__iter__"):
                                erbast_count += len(herd)
                            else: 
                                erbast_count += 0
                        for pride in cell.prides:
                            if pride is not None and hasattr(pride, "__iter__"):
                                carviz_count += len(pride)
                            else:
                                carviz_count += 0
            
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
                        for herd in cell.herds:
                            if herd is not None and hasattr(herd, "__iter__"):
                                erbast_population += len(herd)
                            else: 
                                erbast_population += 0
                        for pride in cell.prides:
                            if pride is not None and hasattr(pride, "__iter__"):
                                carviz_population += len(pride)
                            else:
                                carviz_population += 0
            
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

    import collections.abc as abc

    def start(self):
        self.giveSomeCellsWater()
        self.populateMapWithErbastAndCarviz(0.1, 0.9)
        self.gridStatuses = [self.grid]
        changes = []
        for day in range(NUMDAYS):
            self.growing()
            self.move()
            self.grazing()
            self.struggle()
            self.spawning()
            self.day += 1
            changes.append(self.grid.cells.copy())
            self.gridStatuses.append(copy.deepcopy(self.grid))
            print(f"Day {self.day} completed")
            
        print(self.gridStatuses)


        def heatmaps_build(gridStatuses):
            heatmaps = []

            for grid in gridStatuses:
                heatmap = []
                max_vegetob_density = max(cell.vegetob.density for row in grid.cells for cell in row)
                max_erbast_density = max(len(cell.herds) if isinstance(cell.herds, abc.Iterable) else 0 for row in grid.cells for cell in row)
                max_carviz_density = max(len(cell.prides) if isinstance(cell.prides, abc.Iterable) else 0 for row in grid.cells for cell in row)

                for row in grid.cells:
                    row_colors = []
                    for cell in row:
                        r = int((len(cell.prides) / max_carviz_density) * 255) if isinstance(cell.prides, abc.Iterable) else 0
                        g = int((cell.vegetob.density / 100) * 255)
                        b = int((len(cell.herds) / max_erbast_density) * 255) if isinstance(cell.herds, abc.Iterable) else 0
                        cell_color = (r, g, b)
                        row_colors.append(cell_color)
                    heatmap.append(row_colors)

                heatmaps.append(heatmap)

            return heatmaps
        
        def plot_heatmap_array(heatmaps):
            fig, ax = plt.subplots()
            ax.set_title("Heatmap Evolution")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")

            current_index = 0
            im = ax.imshow(heatmaps[current_index], origin='lower', extent=[0, len(heatmaps[current_index][0]), 0, len(heatmaps[current_index])])
            plt.colorbar(im, ax=ax, label="Density")

            def update_heatmap(index):
                im.set_data(heatmaps[index])
                ax.set_title(f"Heatmap for Day {index}")

            def animate(index):
                update_heatmap(index)

            ani = FuncAnimation(fig, animate, frames=len(heatmaps), interval=1000)
            plt.show()

        heatmaps = heatmaps_build(self.gridStatuses)
        plot_heatmap_array(heatmaps)

        self.plot_terrain()
        self.vegetobDensityPlot()
        self.plotAverageCarvizErbastPopulation()
        self.plotPopulationScatter()
    



