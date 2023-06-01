import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Vegetob:
    def __init__(self, density):
        if density < 0 or density > 100:
            raise ValueError("Density must be between 0 and 100")
        self.density = density
    
    def __str__(self):
        return f"Vegetob: density:{self.density}"



