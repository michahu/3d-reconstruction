# for justin: ```sudo service binfmt-support start``` before running this file
import argparse
import os
import subprocess
import numpy as np
from parseBundleOut import parseFile
import configparser as cp
from emd import emd
import matplotlib.pyplot as plt
import time
import gzip
import shutil
import math

GROUND_TRUTH_FILENAME = "gold.out"
BUNDLER_OUT_FILENAME = "bundle.out"

def read_or_create_gold_bundle(bundler_loc: str, data_loc: str) -> np.array:
    bundle_out_loc = os.path.join(data_loc, "bundle")
    ground_truth_path = os.path.join(bundle_out_loc, GROUND_TRUTH_FILENAME)

    if not GROUND_TRUTH_FILENAME in os.listdir(bundle_out_loc):
        rc = subprocess.call([bundler_loc])
        os.rename(os.path.join(bundle_out_loc, BUNDLER_OUT_FILENAME), ground_truth_path)


    return np.array(parseFile(ground_truth_path, save_path='', toNpz=False))

# unzips all gzipped sift key files in directory
def unzip_sift_keys():
    for file_name in os.listdir():
        if file_name.endswith('.gz'):
            with gzip.open(file_name, 'rb') as f_in:
                with open(os.path.splitext(file_name)[0], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

def plot_camera_losses(gold_bundle: np.array, config: cp.ConfigParser, n_start: int, n_end: int, step: int, to_npz=True):

    full_list_loc = config['Options']['IMAGE_LIST']
    partial_list_loc = 'list_partial.txt'

    # config ensures that bundler skips re-creating SIFT features
    # and uses the partial reconstruction image list
    tmp_config_file = 'bundler.config.tmp'
    new_config = cp.ConfigParser()
    # preserve case: https://stackoverflow.com/questions/1611799/preserve-case-in-configparser
    new_config.optionxform = str
    new_config['Options'] = {'IMAGE_LIST': partial_list_loc,
                            'SKIP_FEATURES': 'true'}
    with open(tmp_config_file, 'w+') as configfile:
        # otherwise bundler will throw command-not-found
        new_config.write(configfile, space_around_delimiters=False)

    x = np.array(range(n_start, n_end+1, step))
    y = np.zeros(len(x))

    with open(full_list_loc, 'r') as image_list:
        image_paths = image_list.read().split('\n')
    image_paths = list(map(lambda x: f'{x}\n', image_paths))
    unzip_sift_keys()
    # create new partial list file if it doesn't already exist
    partial_list_file = open(partial_list_loc, 'w+')
    partial_list_file.close()
    # incrementally build a list of imgs for reconstruction and run
    # bundler on them
    j=0
    for i in range(n_start, n_end+1, step):
        chunk = image_paths[i:min(i+step, n_end+1)]
        if not chunk:
            continue
        with open(partial_list_loc, 'a') as partial_list:
            partial_list.write(''.join(chunk))
        # bundler assumes keypoint matching so it needs at least two images
        if (step == 1 and i == n_start):
            y[j] = math.inf
            j += 1
            continue
        subprocess.call([config['Options']['bundler'], tmp_config_file])
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
    plt.figure()
    plt.plot(x, y)
    plt.show()
    if to_npz:
        np.savez(f'partial-{time.strftime("%Y%m%d-%H%M%S")}', x, y)

def main(args):
    data_loc = os.path.abspath(args.data_loc)
    bundler_loc = os.path.abspath(args.bundler_loc)
    config_loc = os.path.abspath(args.config_file)
    # RunBundler.sh assumes that the working dir is where the data lives
    os.chdir(data_loc)

    gold_bundle = read_or_create_gold_bundle(bundler_loc, data_loc)
    config = cp.ConfigParser()
    config.read(config_loc)
    config['Options']['bundler'] = bundler_loc
    config['Options']['bundle'] = f'bundle/{BUNDLER_OUT_FILENAME}'
    plot_camera_losses(gold_bundle, config, int(args.start_idx), int(args.end_idx), int(args.step), bool(args.to_npz))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_loc", help="path to folder containing the reconstruction images", default="data/ET")
    parser.add_argument("--bundler_loc", help="path to the RunBundler.sh file", default="../bundler_sfm/RunBundler.sh")
    parser.add_argument("--config_file", help="path to bundler config file as in bundler_sfm", default="bundler.config")
    parser.add_argument("--start_idx", default=0, help="index of image in list.txt you want to start reconstruction from")
    parser.add_argument("--end_idx", help="index of image in list.txt you want to end reconstruction with")
    parser.add_argument('--to_npz', action='store_true', help='write the losses and corresponding camera numbers to npz')
    parser.add_argument("--step", default=2, help="number of images to add at a time")
    args = parser.parse_args()
    main(args)
