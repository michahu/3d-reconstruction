from bootstrap import *
from parseBundleOut import parseFile
from emd import emd

import argparse
import math
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import time

def plot_camera_losses(config: cp.ConfigParser, n_start: int, n_end: int, step: int, to_npz=True):

    full_list_loc = config['Options']['IMAGE_LIST']
    bootstrap(config['Options']['bundler'], config['Options']['data_loc'], image_list=PARTIAL_IMAGE_LIST_FILENAME, create_gold=False)
    gold_bundle = read_or_create_gold_bundle(config['Options']['bundler'])
    x = np.array(range(n_start, n_end+1, step))
    y = np.zeros(len(x))

    create_partial_image_list()
    # incrementally build a list of imgs for reconstruction and run
    # bundler on them
    j=0
    for i in range(n_start, n_end+1, step):
        update_partial_image_list(i, n_end, step)
        # bundler assumes keypoint matching so it needs at least two images
        if (step == 1 and i == n_start):
            y[j] = math.inf
            j += 1
            continue
        subprocess.call([config['Options']['bundler'], TMP_CONFIG_FILE])
        partial_bundle = np.array(parseFile(config['Options']['bundle'], '', False), dtype=float)
        assert(len(partial_bundle) <= len(gold_bundle))
        partial_bundle_padded = np.zeros((len(gold_bundle), 3))
        partial_bundle_padded[0:len(partial_bundle)] = partial_bundle
        partial_bundle_padded[len(partial_bundle):] = np.mean(partial_bundle, axis=0)
        y[j] = emd(partial_bundle_padded, gold_bundle)
        j = j+1

    x = list(map(lambda k: min(n_end+1, k+step), x))
    print(x)
    print(y)
    fig = plt.figure()
    plt.plot(x, y)
    plt.xlabel('Num. of Cameras')
    plt.ylabel('Earth-Mover\'s Distance (EMD)')
    plt.title('ET Reconstruction Loss')
    plt.show()
    if to_npz:
        np.savez(f'partial-{time.strftime("%Y%m%d-%H%M%S")}', x, y)

def main(args):
    data_loc = os.path.abspath(args.data_loc)
    bundler_loc = os.path.abspath(args.bundler_loc)
    config_loc = os.path.abspath(args.config_file)

    config = cp.ConfigParser()
    config.read(config_loc)
    config['Options']['bundler'] = bundler_loc
    config['Options']['bundle'] = f'bundle/{BUNDLER_OUT_FILENAME}'
    config['Options']['data_loc'] = data_loc
    plot_camera_losses(config, int(args.start_idx), int(args.end_idx), int(args.step), bool(args.to_npz))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_loc", help="path to folder containing the reconstruction images", default="data/kermit")
    parser.add_argument("--bundler_loc", help="path to the RunBundler.sh file", default="../bundler_sfm/RunBundler.sh")
    parser.add_argument("--config_file", help="path to bundler config file as in bundler_sfm", default="bundler.config")
    parser.add_argument("--start_idx", default=0, help="index of image in list.txt you want to start reconstruction from")
    parser.add_argument("--end_idx", help="index of image in list.txt you want to end reconstruction with")
    parser.add_argument('--to_npz', default=False, action='store_true', help='write the losses and corresponding camera numbers to npz')
    parser.add_argument("--step", default=2, help="number of images to add at a time")
    args = parser.parse_args()
    main(args)