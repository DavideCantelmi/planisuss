### Game constants

NUMDAYS = 150 # Length of the simulation in days

# geometry
NUMCELLS = 20  # size of the (square) grid (NUMCELLS x NUMCELLS)
NUMCELLS_R = 100    # number of rows of the (potentially non-square) grid
NUMCELLS_C = 100    # number of columns of the (potentially non-square) grid

# social groups
NEIGHBORHOOD = 1     # radius of the region that a social group can evaluate to decide the movement
NEIGHBORHOOD_E = 1   # radius of the region that a herd can evaluate to decide the movement
NEIGHBORHOOD_C = 1   #  radius of the region that a pride can evaluate to decide the movement

MAX_HERD = 30  # maximum numerosity of a herd
MAX_PRIDE = 10  # maximum numerosity of a pride

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

WATER_CHANCE = 0.1   # probability of a cell to be water
THRESHOLD_C = 70   # threshold of energy for Carviz to move
THRESHOLD_E = 70    # threshold of energy for Erbast to move