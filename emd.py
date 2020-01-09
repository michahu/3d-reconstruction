from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
import numpy as np

def emd(x1, x2):
    assert len(x1) == len(x2)
    N = len(x1)
    d = cdist(x1, x2)
    assignment = linear_sum_assignment(d)
    return (d[assignment].sum() / N)

if __name__ == '__main__':
    x1 = np.array([1])[:, np.newaxis]
    x2 = np.array([2])[:, np.newaxis]
    emd(x1, x2)
