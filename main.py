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

