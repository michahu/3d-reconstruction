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
import random

GROUND_TRUTH_FILENAME = "gold.out"
BUNDLER_OUT_FILENAME = "bundle.out"
TMP_CONFIG_FILE = 'bundler.config.tmp'
IMAGE_LIST_FILENAME = 'list.txt'
PARTIAL_IMAGE_LIST_FILENAME = 'partial-list.txt'

def create_partial_image_list():
    # create new partial list file if it doesn't already exist
    partial_list_file = open(PARTIAL_IMAGE_LIST_FILENAME, 'w')
    partial_list_file.close()

def update_partial_image_list(start_idx:int, last_idx:int, n:int):
    with open(IMAGE_LIST_FILENAME, 'r') as image_list:
        image_paths = image_list.read().split('\n')
        image_paths = list(map(lambda x: f'{x}\n', image_paths))

    # incrementally build a list of imgs for reconstruction and run
    # bundler on them
    chunk = image_paths[start_idx:min(start_idx+n, last_idx+1)]
    if not chunk:
        return
    with open(PARTIAL_IMAGE_LIST_FILENAME, 'a') as partial_list:
        partial_list.write(''.join(chunk))

def permute_image_list(path=IMAGE_LIST_FILENAME):
    path = os.path.abspath(path)
    with open(path, 'r') as image_list:
        image_paths = image_list.read().split('\n')

    random.shuffle(image_paths)
    with open(path, 'w+') as image_list:
        image_list.write('\n'.join(image_paths))


# read or create a gold bundle from the images in data_loc. assumes that you've already run bootstrap() on the data_loc
def read_or_create_gold_bundle(bundler_loc: str, data_loc='./', config_loc=TMP_CONFIG_FILE, force_create=False) -> np.array:
    bundler_loc = os.path.abspath(bundler_loc)
    data_loc = os.path.abspath(data_loc)

    bundle_out_loc = os.path.join(data_loc, "bundle")
    ground_truth_path = os.path.join(bundle_out_loc, GROUND_TRUTH_FILENAME)

    if force_create or GROUND_TRUTH_FILENAME not in os.listdir(bundle_out_loc):
        rc = subprocess.call([bundler_loc, config_loc])
        os.rename(os.path.join(bundle_out_loc, BUNDLER_OUT_FILENAME), ground_truth_path)

    return np.array(parseFile(ground_truth_path, save_path='', toNpz=False))

# unzips all gzipped sift key files in directory dir
def unzip_sift_keys(dir=os.curdir):
    for file_name in os.listdir(dir):
        if file_name.endswith('.gz'):
            with gzip.open(file_name, 'rb') as f_in:
                with open(os.path.splitext(file_name)[0], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

# prepares a data directory to run bundler in; bundler_loc and data_loc are relative from current directory, image_list is relative from data_loc
def bootstrap(bundler_loc, data_loc, image_list=IMAGE_LIST_FILENAME, create_gold=False):
    data_loc = os.path.abspath(data_loc)
    bundler_loc = os.path.abspath(bundler_loc)

    os.chdir(data_loc)
    shutil.copy(IMAGE_LIST_FILENAME, PARTIAL_IMAGE_LIST_FILENAME)
    # config ensures that bundler skips re-creating SIFT features
    # and uses the partial reconstruction image list
    new_config = cp.ConfigParser()
    # preserve case: https://stackoverflow.com/questions/1611799/preserve-case-in-configparser
    new_config.optionxform = str
    new_config['Options'] = {'IMAGE_LIST': image_list,
                            'SKIP_FEATURES': 'true'}
    with open(TMP_CONFIG_FILE, 'w+') as configfile:
        # otherwise bundler will throw command-not-found
        new_config.write(configfile, space_around_delimiters=False)

    unzip_sift_keys()

    if create_gold:
        read_or_create_gold_bundle(bundler_loc, data_loc, force_create=True)

def run_bundler(bundler_loc, data_loc, num_images, image_list=IMAGE_LIST_FILENAME):
    create_partial_image_list()
    update_partial_image_list(0, num_images, num_images)
    rc = subprocess.call([bundler_loc, TMP_CONFIG_FILE])
    outpath = os.path.abspath(f"bundle/{BUNDLER_OUT_FILENAME}")
    return np.array(parseFile(outpath, save_path='', toNpz=False))

def main(args):
    data_loc = os.path.abspath(args.data_loc)
    bundler_loc = os.path.abspath(args.bundler_loc)
    n = int(args.num_images)

    bootstrap(bundler_loc, data_loc, PARTIAL_IMAGE_LIST_FILENAME, create_gold=False)
    run_bundler(bundler_loc, data_loc, n)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_loc", help="path to folder containing the reconstruction images", default="data/ET")
    parser.add_argument("--bundler_loc", help="path to the RunBundler.sh file", default="../bundler_sfm/RunBundler.sh")
    parser.add_argument("--num_images", help="first k images to process in the list.txt file")
    args = parser.parse_args()
    main(args)
