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


import numpy as np
import matplotlib.pyplot as plt

class Vegetob:
    def __init__(self, density):
        self.set_density(density)

    def set_density(self, density):
        if density < 0:
            self.density = 0
        elif density > 100:
            self.density = 100
        else:
            self.density = density

    def get_density(self):
        return self.density

class Erbast:
    def __init__(self, lifetime, social_attitude, energy = MAX_ENERGY_E):
        self.energy = energy
        self.lifetime = lifetime if lifetime < MAX_LIFE_E else MAX_LIFE_E
        self.age = 0
        self.social_attitude = social_attitude
        self.neighborhood = NEIGHBORHOOD

    def get_energy(self):
        return self.energy

    def set_energy(self, energy):
        self.energy = energy

    def get_lifetime(self):
        return self.lifetime

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age

    def get_social_attitude(self):
        return self.social_attitude

    def get_neighborhood(self):
        return self.neighborhood

    def set_neighborhood(self, neighborhood):
        self.neighborhood = neighborhood

    def join_herd(self, other):
        if isinstance(other, Erbast) and other in self.herd:
            return "The other individual is already in the herd."

        if isinstance(other, Erbast) and self.age >= 30 and other.age >= 30:
            similarity = abs(self.social_attitude - other.social_attitude)
            distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

            if distance <= NEIGHBORHOOD and similarity <= 0.1:
                self.herd.append(other)
                other.herd.append(self)
                return "Individuals have joined the herd successfully."

            else:
                return "The other individual is too far away or is not compatible with the herd."

        else:
            return "The other individual cannot join the herd."
    
class Carviz:
    NEIGHBORHOOD = 5

    def __init__(self, lifetime, social_attitude, energy = MAX_ENERGY_E):
        self.energy = energy if energy < MAX_ENERGY_E else MAX_ENERGY_E
        self.lifetime = lifetime if lifetime < MAX_LIFE_E else MAX_LIFE_E
        self.age = 0
        self.social_attitude = social_attitude

    def get_energy(self):
        return self.energy

    def set_energy(self, energy):
        self.energy = energy if energy >= 0 else 0

    def get_lifetime(self):
        return self.lifetime

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age

    def get_social_attitude(self):
        return self.social_attitude

    def set_social_attitude(self, social_attitude):
        self.social_attitude = social_attitude if 0 <= social_attitude <= 1 else 0 if social_attitude < 0 else 1

    def hunt(self):
        self.energy += 10

    def move(self):
        self.energy -= 1

    def is_alive(self):
        return self.energy > 0 and self.age < self.lifetime

    def join_pride(self, neighbors):
        num_pride = sum([1 for neighbor in neighbors if isinstance(neighbor, Carviz)])
        pride_attitude = num_pride / self.NEIGHBORHOOD
        if pride_attitude >= self.social_attitude:
            return True
        return False

class Planisuss:
    def simulate(self):
        for day in range(NUMDAYS):
            self.grow()
            self.move()
            self.graze()
            self.struggle()
            self.spawn()

    def grow(self):
        for cell in self.cells:
            cell.grow()

    def move(self):
        for cell in self.cells:
            cell.move()
    
    def graze(self):
        for cell in self.cells:
            cell.graze()
    

    def struggle(self):
        for cell in self.cells:
            cell.struggle()
    

    def spawn(self):
        for cell in self.cells:
            cell.spawn()          


import numpy as np
import matplotlib.pyplot as plt

# Generate random data for demonstration
simulation_time = np.arange(0, 100)  # Simulation time (e.g., days)
carviz_population = np.random.randint(0, MAX_HERD, size=len(simulation_time))
erbast_population = np.random.randint(0, MAX_PRIDE, size=len(simulation_time))
vegetob_density = np.random.randint(0, 100, size=len(simulation_time))

# Logging variables
population_log = []
grid_log = []
individual_log = []

# Define the map_image variable with appropriate dimensions and values
map_image = np.zeros((100, 100))  # Example: 100x100 grid with initial values of 0

# Generate random movement data for demonstration
movement_data = [
    ('Carviz', [(10, 10), (20, 20), (30, 30), (40, 40)]),
    ('Erbast', [(90, 90), (80, 80), (70, 70), (60, 60)])
]

# Plotting trajectories on the map
fig, axes = plt.subplots(1, 1, figsize=(8, 8))

# Plot map_image
axes.imshow(map_image, cmap='Blues')
axes.set_title('Map')

# Plot movement trajectories
for species, trajectory in movement_data:
    x, y = zip(*trajectory)
    axes.plot(y, x, label=species)

axes.legend()
axes.set_xlabel('X')
axes.set_ylabel('Y')
axes.set_xlim(0, 100)
axes.set_ylim(0, 100)
axes.set_aspect('equal')
plt.show()

# Run simulation
for t in simulation_time:
    population_log.append((carviz_population[t], erbast_population[t]))
    grid_log.append(map_image.copy())

    individual_data = {}  # Placeholder for individual data at each time step
    individual_log.append(individual_data)

plt.plot(simulation_time, [p[0] for p in population_log], label='Carviz')
plt.plot(simulation_time, [p[1] for p in population_log], label='Erbast')
plt.xlabel('Time (days)')
plt.ylabel('Numerosity')
plt.legend()
plt.title('Numerosity of Carviz and Erbast over Time (Replay)')
plt.show()
plt.scatter([p[0] for p in population_log], [p[1] for p in population_log])
plt.xlabel('Carviz Numerosity')
plt.ylabel('Erbast Numerosity')
plt.title('Numerosity of Carviz vs. Erbast (Replay)')
plt.show()
fig, axes = plt.subplots(2, 1, figsize=(8, 10))

axes[0].imshow(map_image, cmap='Blues')
for movement in movement_data:
    species, trajectory = movement
    x, y = zip(*trajectory)
    axes[0].plot(y, x, label=species)
axes[0].legend()
axes[0].set_title('Trajectories on Map')

axes[1].plot(simulation_time, carviz_population + erbast_population, label='Population')
axes[1].plot(simulation_time, np.mean([carviz_population, erbast_population], axis=0), label='Average Population')
axes[1].set_xlabel('Time')
axes[1].set_ylabel('Population')
axes[1].legend()
axes[1].set_title('Population of Cell and Average Population')
grid_log = []
for t in simulation_time:
    grid_log.append(map_image.copy())
individual_log = []
for t in simulation_time:
    individual_data = {}  
    individual_log.append(individual_data)

fig, axes = plt.subplots(2, 1, figsize=(8, 10))

axes[0].imshow(grid_log[0], cmap='Blues')
axes[0].set_title('Initial Grid')

# Replay grid-level information
for i, grid in enumerate(grid_log[1:], start=1):
    axes[1].clear()
    axes[1].imshow(grid, cmap='Blues')
    axes[1].set_title(f'Grid at Time {simulation_time[i]}')
    plt.pause(0.1)  # Pause between frames to visualize the evolution

for individual_data in individual_log:

    plt.pause(0.1)  

import pickle

# Save simulation state
simulation_state = {
    'simulation_time': simulation_time,
    'carviz_population': carviz_population,
    'erbast_population': erbast_population,
    'vegetob_density': vegetob_density,
}

with open('simulation_state.pkl', 'wb') as file:
    pickle.dump(simulation_state, file)

# Load simulation state
with open('simulation_state.pkl', 'rb') as file:
    loaded_state = pickle.load(file)

# Assign loaded state to variables
simulation_time = loaded_state['simulation_time']
carviz_population = loaded_state['carviz_population']
erbast_population = loaded_state['erbast_population']
vegetob_density = loaded_state['vegetob_density']
# Assign other variables or parameters from the loaded state

# Adjust simulation parameters based on user interaction or input
# Modify variables or parameters according to user input or GUI interactions

# Run the simulation with updated parameters




