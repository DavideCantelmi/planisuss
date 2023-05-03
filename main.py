### Game constants

NUMDAYS = 100000     # Length of the simulation in days

# geometry
NUMCELLS = 1000      # size of the (square) grid (NUMCELLS x NUMCELLS)
NUMCELLS_R = 1000    # number of rows of the (potentially non-square) grid
NUMCELLS_C = 1000    # number of columns of the (potentially non-square) grid

# social groups
NEIGHBORHOOD = 1     # radius of the region that a social group can evaluate to decide the movement
NEIGHBORHOOD_E = 1   # radius of the region that a herd can evaluate to decide the movement
NEIGHBORHOOD_C = 1   #  radius of the region that a pride can evaluate to decide the movement

MAX_HERD = 1000      # maximum numerosity of a herd
MAX_PRIDE = 100      # maximum numerosity of a pride

# individuals
MAX_ENERGY = 100     # maximum value of Energy
MAX_ENERGY_E = 100   # maximum value of Energy for Erbast
MAX_ENERGY_C = 100   # maximum value of Energy for Carviz

MAX_LIFE = 10000     # maximum value of Lifetime
MAX_LIFE_E = 10000   # maximum value of Lifetime for Erbast
MAX_LIFE_C = 10000   # maximum value of Lifetime for Carviz

AGING = 1            # energy lost each month
AGING_E = 1          # energy lost each month for Erbast
AGING_C = 1          # energy lost each month for Carviz

GROWING = 1          # Vegetob density that grows per day.


import random

NUMCELLS = 10

NUMDAYS = 100

class Cell:
    def __init__(self, x, y, terrain):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.vegetob_density = 0
        self.erbast_list = []
        self.carviz_list = []
        self.neighborhood = []

    def add_erbast(self, erbast):
        self.erbast_list.append(erbast)

    def add_carviz(self, carviz):
        self.carviz_list.append(carviz)

class Vegetob:
    def __init__(self, density):
        self.density = density

class Erbast:
    def __init__(self):
        self.name = "Erbast"
        self.nutrition_value = 2
        self.move_range = 1
        self.herd_size = 10
        self.quantity = 10

    def move(self, grid):
        i, j = self.find_location(grid)
        neighbors = self.find_neighbors(grid, i, j, self.move_range)
        if len(neighbors) > 0:
            new_i, new_j = random.choice(neighbors)
            grid[i][j].remove(self)
            grid[new_i][new_j].append(self)

    def find_location(self, grid):
        for i in range(NUMCELLS):
            for j in range(NUMCELLS):
                if self in grid[i][j]:
                    return i, j

    def find_neighbors(self, grid, i, j, radius):
        neighbors = []
        for di in range(-radius, radius+1):
            for dj in range(-radius, radius+1):
                if abs(di) + abs(dj) <= radius and 0 <= i+di < NUMCELLS and 0 <= j+dj < NUMCELLS:
                    if "ground" in grid[i+di][j+dj]:
                        neighbors.append((i+di, j+dj))
        return neighbors
    
    def graze(self, grid):
        i, j = self.find_location(grid)
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if 0 <= i+di < NUMCELLS and 0 <= j+dj < NUMCELLS:
                    for plant in grid[i+di][j+dj]:
                        if isinstance(plant, Vegetob):
                            self.quantity += plant.nutrition_value
                            plant.quantity -= plant.nutrition_value
                            if plant.quantity < 0:
                                grid[i+di][j+dj].remove(plant)

class Carviz:
    def __init__(self, energy, lifetime, social_attitude):
        self.energy = energy
        self.lifetime = lifetime

grid = [[None for _ in range(NUMCELLS)] for _ in range(NUMCELLS)]

for i in range(NUMCELLS):
    for j in range(NUMCELLS):
        if i == 0 or j == 0 or i == NUMCELLS-1 or j == NUMCELLS-1:
            grid[i][j] = "water"
        else:
            if random.random() < 0.5:
                grid[i][j] = "ground"
            else:
                grid[i][j] = "water"

# Define a function to find the neighboring cells of a given position
def find_neighbors(position, move_range):
    neighbors = []
    for i in range(position[0]-move_range, position[0]+move_range+1):
        for j in range(position[1]-move_range, position[1]+move_range+1):
            if i >= 0 and i < NUMCELLS and j >= 0 and j < NUMCELLS and (i,j) != position:
                neighbors.append((i,j))
    return neighbors

def update_grid():
    new_grid = [[None for _ in range(NUMCELLS)] for _ in range(NUMCELLS)]
    for i in range(NUMCELLS):
        for j in range(NUMCELLS):
            if grid[i][j] == "ground":
                if "Vegetob" in grid[i][j]:
                    new_vegetob = int(grid[i][j]["Vegetob"] * (1 + Vegetob().growth_rate))
                    new_vegetob = min(new_vegetob, 9)
                    new_grid[i][j] = {"Vegetob": new_vegetob}
                elif "Erbast" in grid[i][j]:
                    if random.random() < 0.5:
                        neighbors = find_neighbors


# Run the simulation for NUMDAYS days
for day in range(NUMDAYS):
    update_grid()

# TODO: analyze the results of the simulation and plot any necessary graphs or charts
