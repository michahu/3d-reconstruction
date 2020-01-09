#!/usr/local/bin/python3

import sys
import numpy as np
# need to install scikit learn
# documentation: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
from sklearn.decomposition import PCA
from emd import emd

num_sectors = 16
num_pca_components = 3

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

def compute_x(points, cameras):

  def compute_PCA_components(points):
    # compute PCA vectors
    pca = PCA(n_components=3)
    pca.fit(points)
    return pca.components_.flatten() # returns a 1 x 9 vector
  
  def get_center(points):
    return np.mean(points, axis=0)[:2]

  # compute camera sectors

  def compute_sectors(cameras, points):
    ret = [0] * 16
    center = get_center(points)
    for camera in cameras:
      camera = camera['trans']
      d = get_camera_angle(camera, center)
      sector = get_sector(d)
      ret[sector] = 1
    return ret
  
  pca_components = compute_PCA_components(points)
  camera_sectors = compute_sectors(cameras, points)
  return np.concatenate((pca_components, camera_sectors), axis=None)

def compute_y(best: "Description of scene with all cameras",
              datum: "Array of Data loaded from parsed npz") -> "Discretized cam vec":
  losses = [emd(best['points'], dat['points']) for dat in datum]
  best_idx = np.argmin(losses)
  return compute_x(datum[best_idx])

def construct_training_set():
  pass

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Usage: ./compose_data.py <parseBundleOut all cameras> <parseBundleOut some # of cams>")
    exit()
  best = np.load(sys.argv[1], allow_pickle=True)
  data = [np.load(f, allow_pickle=True) for f in sys.argv[2:]]
  compute_y(best, data)

  with np.load(sys.argv[1]) as data:
    points = data['points']
    print(points)
    cams = data["cameras"]
    print(cams)
    x = compute_x(points, cams)
    y = 


