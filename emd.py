from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
import numpy as np

def emd(x1, x2):
  if len(x1) < len(x2):
    print(x2.shape)
    x1 = np.pad(x1, np.subtract(x1.shape, x2.shape)/2, mode='mean')
  elif  len(x1) > len(x2):
    x2 = np.pad(x2, 1, mode='mean')
  print(x1.shape)
  print(x2.shape)
  exit()
  N = len(x1)
  d = cdist(x1, x2)
  assignment = linear_sum_assignment(d)
  return (d[assignment].sum() / N)

if __name__ == '__main__':
  x1 = np.array([1])[:, np.newaxis]
  x2 = np.array([2])[:, np.newaxis]
  emd(x1, x2)
