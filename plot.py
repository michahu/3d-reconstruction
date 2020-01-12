from bootstrap import *
from parseBundleOut import parseFile
from emd import emd

import argparse
import math
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import time

def create_out_npz(args, n_start: int, n_end: int, step: int):
    bundle = f'bundle/{BUNDLER_OUT_FILENAME}'
    create_partial_image_list()
    j=0
    for i in range(n_start, n_end+1, step):
        update_partial_image_list(i, n_end, step)
        # bundler assumes keypoint matching so it needs at least two images
        if (step == 1 and i == n_start):
            y[j] = math.inf
            j += 1
            continue
        subprocess.call([args.bundler_loc, TMP_CONFIG_FILE])
        partial_bundle = np.array(parseFile(bundle, f'partial-ND-perm2-{i+step}', True), dtype=float)

def plot_camera_losses(args, n_start: int, n_end: int, step: int, to_npz=True):
    bundle = f'bundle/{BUNDLER_OUT_FILENAME}'
    gold_bundle = read_or_create_gold_bundle(args.bundler_loc)
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
        subprocess.call([args.bundler_loc, TMP_CONFIG_FILE])
        partial_bundle = np.array(parseFile(bundle, '', False), dtype=float)
        y[j] = emd(partial_bundle, gold_bundle)
        j = j+1

    x = list(map(lambda k: min(n_end+1, k+step), x))
    fig = plt.figure()
    plt.plot(x, y)
    plt.xlabel('Num. of Cameras')
    plt.ylabel('Earth-Mover\'s Distance (EMD)')
    plt.title('ET Reconstruction Loss')
    plt.show()
    if to_npz:
        np.savez(f'partial-{time.strftime("%Y%m%d-%H%M%S")}', x, y)


def plot_permutation_loss(args, n_start: int, n_end: int, step: int, to_npz=True):
    permute_image_list()
    plot_camera_losses(args, n_start, n_end, step, to_npz)

def main(args):
    args.data_loc = os.path.abspath(args.data_loc)
    args.bundler_loc = os.path.abspath(args.bundler_loc)
    args.config_loc = os.path.abspath(args.config_file)

    bootstrap(args.bundler_loc, args.data_loc, image_list=PARTIAL_IMAGE_LIST_FILENAME, create_gold=False)

    if args.permute:
        permute_image_list()
        create_out_npz(args, int(args.start_idx), int(args.end_idx), int(args.step))
        # plot_permutation_loss(args, int(args.start_idx), int(args.end_idx), int(args.step), bool(args.to_npz))
    else:
        # plot_camera_losses(args, int(args.start_idx), int(args.end_idx), int(args.step), bool(args.to_npz))
        create_out_npz(args, int(args.start_idx), int(args.end_idx), int(args.step))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_loc", help="path to folder containing the reconstruction images", default="data/NotreDame/non_rd_images")
    parser.add_argument("--bundler_loc", help="path to the RunBundler.sh file", default="../bundler_sfm/RunBundler.sh")
    parser.add_argument("--config_file", help="path to bundler config file as in bundler_sfm", default="bundler.config")
    parser.add_argument("--start_idx", default=0, help="index of image in list.txt you want to start reconstruction from")
    parser.add_argument("--end_idx", help="index of image in list.txt you want to end reconstruction with")
    parser.add_argument("--step", default=2, help="number of images to add at a time")
    parser.add_argument("--permute", default=False, action='store_true', help='permute the list of images')
    parser.add_argument('--to_npz', default=False, action='store_true', help='write the losses and corresponding camera numbers to npz')
    args = parser.parse_args()
    main(args)
