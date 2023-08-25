import numpy as np

def normalise(v):
    """ 
    Normalise a vector to length 1 (used for keeping agents speed to 1)
    """
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm