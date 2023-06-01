import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import *

class Erbast: 
    def __init__(self,energy,lifetime,age,socialAttitude):
        self.energy = min(energy, MAX_ENERGY_E)
        if self.energy < 0:
            raise ValueError("energy must be positive")
        self.lifetime = min(lifetime, MAX_LIFE_E)
        if age < 0 or age > lifetime:
            raise ValueError("age must be between 0 and lifetime")
        self.age = age
        if socialAttitude < 0 or socialAttitude > 1:
            raise ValueError("socialAttitude must be between 0 and 1")
        self.socialAttitude = socialAttitude 
        self.living = True
    
    def __str__(self):
        return f"Erbast: energy:{self.energy}, lifetime:{self.lifetime}, age:{self.age}, socialAttitude:{self.socialAttitude}"
    
    def ageUp(self):
        self.age += 1
        if self.age > self.lifetime:
            self.living = False
    
    def isLiving(self):
        return self.living