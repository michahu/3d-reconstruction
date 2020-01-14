from scipy.spatial.distance import cdist
from emd import calc_distance
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.style as style
from matplotlib import rc


if __name__=='__main__':
    # t_cdist, t_par, t_32 = [],[],[]
    # for i in range(1, 16):
    #     x = np.random.rand(2**i, 3)
    #     y = np.random.rand(2**i, 3)
    #     start= time.time()
    #     cdist(x, y)
    #     t_cdist.append(time.time() - start)
    #     start = time.time()
    #     calc_distance(x, y)
    #     t_par.append(time.time() - start)
    #     x = x.astype(np.float32)
    #     y = y.astype(np.float32)
    #     start = time.time()
    #     calc_distance(x, y)
    #     t_32.append(time.time() - start)
    # np.savez('timings', t_cdist, t_par, t_32, 't_cdist', 't_par', 't_32')
    # https://medium.com/@andykashyap/top-5-tricks-to-make-plots-look-better-9f6e687c1e08
    style.use('seaborn-dark-palette')
    t_cdist = np.load('timings.npz')['arr_0']
    t_par = np.load('timings.npz')['arr_1']
    t_32 = np.load('timings.npz')['arr_2']
    plt.plot(range(1, 16), t_cdist, marker='d', linestyle=':')
    plt.plot(range(1, 16), t_par, marker='d', linestyle=':')
    plt.plot(range(1, 16), t_32, marker='d', linestyle=':')
    plt.grid()
    plt.legend(['SciPy cdist', 'Ours Float64', 'Ours Float32'])
    plt.xlabel(r'$\log_2(N)$')
    plt.ylabel(r'Time (s)')
    plt.title('Timing Euclidean Distance Cost Matrix Computation')
    plt.show()