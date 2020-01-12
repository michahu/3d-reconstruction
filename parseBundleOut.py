#!/usr/local/bin/python3

# might need to adjust above line to point at version of python3

# note: this script doesn't work if the file cannot be held in memory.
# current implementation should work, as bundler outfiles are less than 1GB

# usage: python parseBundleOut.py /path/to/file.out /path/to/new/file
# can also import the method
# Saves as a npz file.

# Load instructions:
# data = np.load(/path/to/new/file.npz)
# points = data['points'] <-- loads as a numpy array

import sys
import numpy as np

# saves parsed file to .npz file
def parseFile(file, toNpz=True):
    with open(file, 'r') as f:
      lines = f.readlines()
      N = len(lines)
      # print(f'NUMBER OF POINTS: {lines[1].split()[1]}')
      n_cams, n_points = map(int, lines[1].split())

      pts = []
      for i in range(1, n_points + 1):
          index = N - i * 3
          pts.append(np.fromstring(lines[index], sep = " "))
      cams = []
      offset = 2
      # https://github.com/snavely/bundler_sfm#output-format
      for i in range(0, n_cams):
          idx = offset + i * 5
          focal_length, rad_dist1, rad_dist2 = np.fromstring(lines[idx], sep = " ")
          cams.append({
            "focal_length": focal_length,
            "rad_dist1": rad_dist1,
            "rad_dist2": rad_dist2,
            "rot": np.array([np.fromstring(lines[idx+j], sep=" ") for j in range(1, 4)]),
            "trans": np.fromstring(lines[idx+4], sep=" "),
          })

      if toNpz:
          np.savez(file, points=pts, cameras=cams)
      else:
          return np.array(pts)

if __name__ == '__main__':
    if len(sys.argv) < 2:
      print("Usage: ./parseBundleOut.py <bundle.out>")
      exit()
    for f in sys.argv[1:]:
      parseFile(f)
