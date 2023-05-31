import numpy as np

### Game constants

NUMDAYS = 100000     # Length of the simulation in days

# geometry
NUMCELLS = 10     # size of the (square) grid (NUMCELLS x NUMCELLS)
NUMCELLS_R = 100    # number of rows of the (potentially non-square) grid
NUMCELLS_C = 100    # number of columns of the (potentially non-square) grid

# social groups
NEIGHBORHOOD = 1     # radius of the region that a social group can evaluate to decide the movement
NEIGHBORHOOD_E = 1   # radius of the region that a herd can evaluate to decide the movement
NEIGHBORHOOD_C = 1   #  radius of the region that a pride can evaluate to decide the movement

MAX_HERD = 100      # maximum numerosity of a herd
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

GROWING = 1          
HUNGER = 1           

class Cell:
    def __init__(self,x,y,cell_type,vegetobDensity):
        self.x = x
        self.y = y
        self.cell_type = cell_type # water or land
        self.vegetobDensity = vegetobDensity # 0-100
        self.herd = np.empty(0,dtype=Erbast)
        self.pride = np.empty(0,dtype=Carviz)
    #when cast to int retun the vegetobDensity
    # def __int__(self):
    #     return np.dstack((self.vegetobDensity,len(self.herd),len(self.pride)))
    
    def __str__(self):
        return f"{self.x},{self.y}-{len(self.herd)}"
    
    def __int__(self):
        return self.vegetobDensity

    def RGB(self):
        if self.cell_type == "water":
            return [0,0,255]
        else:
            return [len(self.pride)/10*255,len(self.herd)/10*255,self.vegetobDensity/100*255]
    def Green(self):
        return self.vegetobDensity/100*255
        
class Erbast:
    def __init__(self,energy,lifetime,age,socialAttitude):
        self.energy = energy 
        self.lifetime = lifetime 
        self.age = age # 0-lifetime
        self.socialAttitude = socialAttitude # 0-1

class Carviz:
    def __init__(self,energy,lifetime,age,socialAttitude):
        self.energy = energy 
        self.lifetime = lifetime 
        self.age = age # 0-lifetime
        self.socialAttitude = socialAttitude # 0-1

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from matplotlib.widgets import Button
from perlin_noise import PerlinNoise
import random

cell_grid = np.empty((NUMCELLS,NUMCELLS),dtype=Cell)
noise = PerlinNoise(octaves=NUMCELLS/10, seed=np.random.randint(0,100))
pix = NUMCELLS
noise_map = [[int((noise([i/pix, j/pix])+1)*50) for j in range(pix)] for i in range(pix)]

for i in range(NUMCELLS):
    for j in range(NUMCELLS):
        if i == 0 or i == NUMCELLS-1 or j == 0 or j == NUMCELLS-1:
            cell_grid[i][j] = None
        else:
            cell_grid[i][j] = Cell(i,j,"land",noise_map[i][j])
            #for each cell assign a herd of erbast
            cell_grid[i][j].herd = [Erbast(5,50,0,random.choice([0,1]) ) for _ in range(0,random.randint(0,15))]
            cell_grid[i][j].pride = [Carviz(5,50,0,random.choice([0,1]) ) for _ in range(0,random.randint(0,15))]



def gridToRgbArrey(grid):
    return np.array([[grid[i][j].RGB() if grid[i][j] is not None else [0,0,0] for j in range(NUMCELLS)] for i in range(NUMCELLS)]).astype(np.uint8)

def gridToVegetobArrey(grid):
    return np.array([[grid[i][j].vegetobDensity if grid[i][j] is not None else 0 for j in range(NUMCELLS)] for i in range(NUMCELLS)])
def update(frame):
    for i in range(NUMCELLS):
        for j in range(NUMCELLS):
            if cell_grid[i][j] is not None: # check only land cells
                # Update the vegetob density
                cell = cell_grid[i][j]

                cell.vegetobDensity += GROWING
                if cell.vegetobDensity > 100:
                    cell.vegetobDensity = 100

                #get the grid of the neighborhood
                neighborhood = np.array([[cell_grid[i+ii][j+jj] if cell_grid[i+ii][j+jj] is not None else 0 for jj in range(-NEIGHBORHOOD,NEIGHBORHOOD+1)] for ii in range(-NEIGHBORHOOD,NEIGHBORHOOD+1)])
                
                if i == len(cell_grid)-2 and j == len(cell_grid)-2:
                    print(neighborhood.astype(str))

    # Update the display
    im.set_data(gridToVegetobArrey(cell_grid))
    return [im]

# Create the display
rgb_grid = gridToRgbArrey(cell_grid)

vegetob_grid = np.array([[cell_grid[i][j].vegetobDensity if cell_grid[i][j] is not None else 0 for j in range(NUMCELLS)] for i in range(NUMCELLS)])
carviz_grid = np.array([[len(cell_grid[i][j].pride) if cell_grid[i][j] is not None else 0 for j in range(NUMCELLS)] for i in range(NUMCELLS)])
erbast_grid = np.array([[len(cell_grid[i][j].herd) if cell_grid[i][j] is not None else 0 for j in range(NUMCELLS)] for i in range(NUMCELLS)])

fig, ax = plt.subplots(2,2)
im = ax[0][0].imshow(vegetob_grid, cmap='Greens', vmax=100, vmin=0)

anim = animation.FuncAnimation(fig, update, frames=1, interval=1000, blit=True)

ax_pause = plt.axes([0.8, 0, 0.20, 0.085]) 
bpause = Button(ax_pause, 'Stop')

def pause(event):
    anim.pause()

bpause.on_clicked(pause)

plt.show()