import sys 
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from constants import *
from src.simulation.simulation import Simulation

if __name__ == "__main__":
    simulation = Simulation()
    simulation.start()