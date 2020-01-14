from scipy.spatial.distance import cdist
from lapjv import lapjv
import numpy as np
import numba as nb
import math
import time
import matplotlib.pyplot as plt

# pads a to the size of b
def pad(a, b):
  a = a.astype(np.float32)
  b = b.astype(np.float32)

  if len(a) == len(b):
    return a, b
  elif len(a) > len(b):
    tmp = np.zeros((len(a), 3), dtype=np.float32)
    tmp[0:len(b)] = b
    tmp[len(b):] = np.mean(b, axis=0)
    b = tmp
  else:
    tmp = np.zeros((len(b), 3), dtype=np.float32)
    tmp[0:len(a)] = a
    tmp[len(a):] = np.mean(a, axis=0)
    a = tmp
  return a, b

# https://stackoverflow.com/questions/49487399/efficient-way-to-compute-element-wise-euclidiant-distance-between-two-3d-matrice/49490630#49490630
@nb.njit(fastmath=True,parallel=True)
def calc_distance(vec_1,vec_2):
    assert vec_1.shape[1]==3 #Enable SIMD-Vectorization (adding some performance)
    assert vec_2.shape[1]==3 #Enable SIMD-Vectorization (adding some performance)

    res=np.empty((vec_1.shape[0],vec_2.shape[0]),dtype=vec_1.dtype)
    for i in nb.prange(vec_1.shape[0]):
        for j in range(vec_2.shape[0]):
            res[i,j]=np.sqrt((vec_1[i,0]-vec_2[j,0])**2+(vec_1[i,1]-vec_2[j,1])**2+(vec_1[i,2]-vec_2[j,2])**2)
    return res

def emd(x1, x2):
  x1, x2 = pad(x1, x2)
  N = len(x1)
  start = time.time()
  d = calc_distance(x1, x2)
  print(f'Dimension of Cost matrix: {d.shape}')
  print(f'Pairwise Euclidean distance calc took {time.time() - start} s')
  start = time.time()
  row_idx, col_idx, _ = lapjv(d)
  print(f'LAP took {time.time() - start} s')
  emd = (d[row_idx, col_idx].sum() / N)
  print(f'emd: {emd}')
  return emd

if __name__ == '__main__':
  # arrs = np.load(f'notre-dame-step-10-losses.npz')
  # for key in arrs.keys():
  #   print(key)
  # x = np.load(f'notre-dame-step-10-losses.npz')['arr_0']
  # y = np.load(f'notre-dame-step-10-losses.npz')['arr_1']

  # plt.plot(x, y)
  # plt.show()
  x = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]])
  y = np.array([[0, 0, 0], [1, 1, 1]])
  x, y = pad(x, y)
  print(x)
  print(y)
