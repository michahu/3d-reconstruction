from emd import emd
import numpy as np
import matplotlib.pyplot as plt
import time
import os

losses = dict()
stop = 110
dir = '.'
gold_bundle = np.load(f'{dir}/partial-ND-{stop}.npz')['points']
x, y = [], []
for file_name in os.listdir(f'{dir}'):
  if file_name.startswith('partial-ND'):
    idx = int(file_name.split('-')[-1].split('.')[0])
    if idx >= stop:
       break
    bundle = np.load(f'{dir}/{file_name}')['points']
    start = time.time()
    losses[idx] = emd(gold_bundle, bundle)
    print(f'Processed {file_name} in {time.time() - start}s')

for idx in sorted(losses):
  x.append(idx)
  y.append(losses[idx])

np.savez('notre-dame-step-10-losses', x, y)
plt.plot(x, y)
plt.show()
