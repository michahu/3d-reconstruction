import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np
import os

if __name__=='__main__':
    fig = plt.figure()
    style.use('seaborn-dark-palette')
    x = np.load('notre-dame-step-10-losses-orig.npz')['arr_0']
    y = np.load('notre-dame-step-10-losses-orig.npz')['arr_1']
    plt.plot(x, y, marker='d', linestyle=':')
    x = np.load('notre-dame-step-10-losses-perm1.npz')['arr_0']
    y = np.load('notre-dame-step-10-losses-perm1.npz')['arr_1']
    plt.plot(x, y, marker='d', linestyle=':')
    x = np.load('notre-dame-step-10-losses-perm2.npz')['arr_0']
    y = np.load('notre-dame-step-10-losses-perm2.npz')['arr_1']
    plt.plot(x, y, marker='d', linestyle=':')
    x = np.load('notre-dame-step-10-losses-perm3.npz')['arr_0']
    y = np.load('notre-dame-step-10-losses-perm3.npz')['arr_1']
    plt.plot(x, y, marker='d', linestyle=':')
    plt.ylabel('EMD')
    plt.xlabel('Number of Images')
    plt.legend(['R1', 'R2', 'R3', 'R4'])
    plt.title('Reconstruction Loss for Image Sequence Permutations')
    plt.grid()
    plt.show()
