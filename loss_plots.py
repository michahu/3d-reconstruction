
import argparse
import os
import subprocess
import numpy as np

def read_or_create_gold_bundle(bundler_loc, data_loc):
    if not "bundle.out" in os.listdir(os.path.join(data_loc, "bundle")):
        os.chdir(data_loc)
        rc = subprocess.call([bundler_loc])

def main(args):
    data_loc = os.path.abspath(args.data_loc)
    bundler_loc = os.path.abspath(args.bundler_loc)
    config_loc = os.path.abspath(args.config_file)

    gold_bundle = read_or_create_gold_bundle(bundler_loc, data_loc)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_loc", help="path to folder containing the reconstruction images")
    parser.add_argument("--bundler_loc", help="path to the RunBundler.sh file")
    parser.add_argument("--config_file", help="path to bundler config file as in bundler_sfm")
    args = parser.parse_args()
    main(args)
