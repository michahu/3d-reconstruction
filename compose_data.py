#!/usr/local/bin/python3

import sys
import numpy as np
# need to install scikit learn
# documentation: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
from sklearn.decomposition import PCA

num_sectors = 16
num_pca_components = 3

def compute_x(input_data):
  r, c = input_data.shape
  assert(c == 3)

  def compute_PCA_components(points_data):
    # compute PCA vectors
    pca = PCA(n_components=3)
    pca.fit(input_data)
    return pca.components_.flatten() # returns a 1 x 9 vector

  # compute camera sectors
  def compute_sectors():
    # TODO: compute camera sector vector
    pass

  pass

def compute_y():
  pass

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: ./compose_data.py <Output from parseBundleOut.py>")
    exit()
  with np.load(sys.argv[1]) as data:
    points = data['points']
    print(points)
    cams = data["cameras"]
    print(cams)
