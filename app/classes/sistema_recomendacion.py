import numpy as np
from itertools import combinations
import copy
from time import sleep

# Define las opiniones
opiniones = [
    "2, 1, 6, 7, 8",
    "2, 1, 6, 7, 8",
    "2, 1, 4, 9, 6, 7, 8",
    # ...
]

class SistemaRecomendacion():
    
    

    palabras_vacias = set(
