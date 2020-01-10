#!/usr/local/bin/python3

import sys
import os
import numpy as np
import argparse
from collections import defaultdict

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
    # the output is sometimes degenerate
    if data2[index] == []:
      continue
    data2[index] = np.array(data2[index])
    print(data2[index])
    r_indices, r_data = data2[index][:, 0], data2[index][:, 1]
    xi = compute_x(datum[0])
    #print(xi)
    #print(r_indices)
    #print(r_data)
    yi = compute_y(best, r_indices, r_data)
    x.append(xi)
    y.append(yi)
    #print(xi, yi)
  np.savez(save_path, x=x, y=y)
  return x, y

def main(args):
  data1_loc = os.path.abspath(args.pre)
  # print(f'data1_loc: {data1_loc}')
  data2_loc = os.path.abspath(args.post)
  # print(f'data2_loc: {data2_loc}')

  best = np.load(args.gold_label, allow_pickle=True)

  data1 = defaultdict(list)
  for f in os.listdir(data1_loc):
    s = f.split('_')
    s1 = s[1:-1][0]
    s2 = s[-1].split('.')[0]
    int_s = int(s1 + s2)
    # print(int_s)
    datum = np.load(data1_loc + '/' + f, allow_pickle=True)
    data1[int_s].append(datum)

  data2 = defaultdict(list)
  for f in os.listdir(data2_loc):
    s = f.split('_')[1:]
    s1 = int(''.join(s[:-1]))
    s2 = int(s[-1].split('.')[0]) #s2: the end string
    # print(s1, s2)
    datum = np.load(data2_loc + '/' + f, allow_pickle=True)
    data2[s1].append([s2, datum])

    # what this data structure looks like:
    # data = {
    # 5 -> [[6, datum], [7, datum]]
    # 6 -> [[5, datum], [2, datum]]
    # }

  x, y = construct_training_set(best, data1, data2, args.save_path)
  print(x, y)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--gold_label", help="path to gold label file")
  parser.add_argument("--pre", help="path to files")
  parser.add_argument("--post", help="path to files after 1 step")
  parser.add_argument("--save_path", help="save_path")
  args = parser.parse_args()

  # Sample command:
  # python3 compose_data.py --gold_label=./bin/et/9/*.npz --pre=./bin/et/2 --post=./bin/et/3 --save_path=test.npz

  print(args)
  main(args)
