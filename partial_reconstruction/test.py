import os
import numpy as np

if __name__=='__main__':
    for file_name in os.listdir(os.curdir):
        if file_name.startswith('partial-ND'):
            idx = int(file_name.split('-')[-1].split('.')[0])
            bundle = np.load(f'{file_name}')['points']
            print(f'{idx}: {len(bundle)}')