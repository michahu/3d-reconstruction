#!/usr/local/bin/python3

import sys
import numpy as np


num_sectors = 16
num_pca_components = 3

def compute_x(input_data):
  r, c = input_data.shape
  assert(c == 3)
  pass

def compute_y():
  pass

np.load("kermit_points.npz")

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: ./compose_data.py <Output from parseBundleOut.py>")
    exit()
  with np.load(sys.argv[1]) as data:
    print(data['points'])
