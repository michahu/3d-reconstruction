#!/usr/local/bin/python3

import sys
import numpy as np
# need to install scikit learn
# documentation: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
from sklearn.decomposition import PCA
from emd import emd

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

def compute_y(best: "Description of scene with all cameras",
              datum: "Array of Data loaded from parsed npz") -> "Discretized cam vec":
  losses = [emd(best['points'], dat['points']) for dat in datum]
  best_idx = np.argmin(losses)
  return compute_x(datum[best_idx])

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Usage: ./compose_data.py <parseBundleOut all cameras> <parseBundleOut some # of cams>")
    exit()
  best = np.load(sys.argv[1], allow_pickle=True)
  data = [np.load(f, allow_pickle=True) for f in sys.argv[2:]]
  compute_y(best, data)
