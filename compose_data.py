#!/usr/local/bin/python3

import sys
import numpy as np
# need to install scikit learn
# documentation: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
from sklearn.decomposition import PCA
from emd import emd

def get_sector(d):
  if d > np.pi * -1 / 16 and d < np.pi * 1 / 16:
    return 0
  elif d > np.pi * 1 / 16 and d < np.pi * 3 / 16:
    return 1
  elif d > np.pi * 3 / 16 and d < np.pi * 5 / 16:
    return 2
  elif d > np.pi * 5 / 16 and d < np.pi * 7 / 16:
    return 3
  elif d > np.pi * 7 / 16 and d < np.pi * 9 / 16:
    return 4
  elif d > np.pi * 9 / 16 and d < np.pi * 11 / 16:
    return 5
  elif d > np.pi * 11 / 16 and d < np.pi * 13 / 16:
    return 6
  elif d > np.pi * 13 / 16 and d < np.pi * 15 / 16:
    return 7
  elif d > np.pi * 15 / 16 or d < np.pi * -15 / 16:
    return 8
  elif d > np.pi * -15 / 16 and d < np.pi * -13 / 16:
    return 9
  elif d > np.pi * -13 / 16 and d < np.pi * -11 / 16:
    return 10
  elif d > np.pi * -11 / 16 and d < np.pi * -9 / 16:
    return 11
  elif d > np.pi * -9 / 16 and d < np.pi * -7 / 16:
    return 12
  elif d > np.pi * -7 / 16 and d < np.pi * -5 / 16:
    return 13
  elif d > np.pi * -5 / 16 and d < np.pi * -3 / 16:
    return 14
  else:
    return 15

def get_camera_angle(camera, center):
  # camera: (x, y, z)
  # center: (x, y, z)
  dx = camera[0] - center[0]
  dy = camera[1] - center[1]
  return np.arctan2(dx, dy)

def compute_x(datum):
  pts = datum['points']
  cams = datum['cameras']

  def compute_PCA_components(points):
    # compute PCA vectors
    pca = PCA(n_components=3)
    pca.fit(points)
    return pca.components_.flatten() # returns a 1 x 9 vector

  def get_center(points):
    return np.mean(points, axis=0)[:2]

  def compute_sectors(cameras, points):
    ret = [0] * 16
    center = get_center(points)
    for camera in cameras:
      camera = camera['trans']
      d = get_camera_angle(camera, center)
      sector = get_sector(d)
      ret[sector] = 1
    return ret

  pca_components = compute_PCA_components(pts)
  camera_sectors = compute_sectors(cams, pts)
  return np.concatenate((pca_components, camera_sectors), axis=None)

def compute_y(best: "Description of scene with all cameras",
              indices: "camera corresponding to data",
              data: "Array of Data loaded from parsed npz") -> "Discretized cam vec":
  losses = [emd(best['points'], dat['points']) for dat in data]
  ret = [0] * 16
  best_data = indices[np.argmin(losses)]
  ret[best_data] = 1

  return ret

def construct_training_set(best, data1, data2, save_path):
  x = []
  y = []
  for index, datum in data1.items():
    # below line might not work
    r_indices, r_data = data2[index][0, :], data2[index][1, :]
    xi = compute_x(datum)
    yi = compute_y(best, r_indices, r_data)
    x.append(xi)
    y.append(yi)
  np.savez(save_path, x=x, y=y)
  return x, y

if __name__ == "__main__":
  if len(sys.argv) < 5:
    print("Usage: ./compose_data.py <parseBundleOut all cameras> <parseBundleOut preceding> <parseBundleOut some # of cams> <save_path>")
    exit()

  best = np.load(sys.argv[1], allow_pickle=True)

  # bundle_005
  data1 = {}
  for f in sys.argv[2:]:
    s = f.split('_')
    s1 = int(s[1])
    datum = np.load(f, allow_pickle=True)
    data1.get(s1, []).append(datum)

  # bundle_005_006
  data2 = {}
  for f in sys.argv[3:]:
    s = f.split('_')
    s1 = int(s[1]) #s1: the initial string
    s2 = int(s[2]) #s2: the end string
    datum = np.load(f, allow_pickle=True)
    data2.get(s1, []).append([s2, datum])

    # what this data structure looks like:
    # data = {
    # 5 -> [[6, datum], [7, datum]]
    # 6 -> [[5, datum], [2, datum]]
    # }

  x, y = construct_training_set(best, data1, data2, sys.argv[3:])
  print(x, y)

