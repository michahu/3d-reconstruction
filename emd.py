from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
import numpy as np
import math

# pads a to the size of b
def pad(a, b):
  pad_shape = np.subtract(b.shape, a.shape)/2
  pad_shape += 0.1
  pad_shape = np.round(pad_shape)
  return [(math.ceil(v/2.0), math.floor(v/2.0)) for v in pad_shape]

def emd(x1, x2):
  d = cdist(x1, x2)
  assignment = linear_sum_assignment(d)
  return d[assignment].sum()

if __name__ == '__main__':
  x1 = np.array([1])[:, np.newaxis]
  x2 = np.array([2])[:, np.newaxis]
  emd(x1, x2)

  x1 = np.array([1])[:, np.newaxis]
  x2 = np.array([2, 3])[:, np.newaxis]
  emd(x1, x2)
