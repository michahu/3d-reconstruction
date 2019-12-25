# note: this script doesn't work if the file cannot be held in memory.
# current implementation should work, as bundler outfiles are less than 1GB

# usage: python parseBundleOut.py /path/to/file.out /path/to/new/file
# Saves as a npz file.

# Load instructions: 
# data = np.load(/path/to/new/file.npz)
# points = data['points'] <-- loads as a numpy array

import sys
import numpy as np

# prints parsed file line by line
def parseFile(file, save_path):
    f = open(file, 'r')
    lines = f.readlines()
    N = len(lines)
    # print(f'NUMBER OF POINTS: {lines[1].split()[1]}')
    points = int(lines[1].split()[1])

    arr = []
    for i in range(1, points + 1):
        index = N - i * 3
        arr.append(lines[index].split()) 

    np.savez(save_path, points=arr)

if __name__ == '__main__':
    parseFile(sys.argv[1], sys.argv[2])