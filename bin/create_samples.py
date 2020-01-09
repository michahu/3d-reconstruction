#!/usr/local/bin/python3

import os
import itertools
import argparse
import shutil
import re

def fact(n): 1 if n is 0 else n * fact(n-1)

def clean_imgs():
  os.popen("rm *.jpg *.txt *.pgm 2> /dev/null").read()
  os.popen("rm -rf output 2> /dev/null").read()

def create_bundles(bundle_loc, image_dir, num_imgs):
  cwd = os.getcwd()
  os.chdir(bundle_loc)
  clean_imgs()
  imgs = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(".jpg")]
  # if we care about order, we can change this to permutations
  combs = itertools.combinations(imgs, num_imgs)
  nums = re.compile(r'\d')
  print("Num combinations:", len(list(itertools.combinations(imgs, num_imgs))))
  for comb in combs:
    for img in comb: shutil.copy(img, bundle_loc)
    os.popen("ant -f bundle.xml 2> /dev/null").read()
    order = '_'.join([''.join(nums.findall(os.path.basename(img))) for img in comb])
    try:
      shutil.copy(
        os.path.join(bundle_loc, "output", "bundle.out"),
        os.path.join(cwd, f'bundle_{order}.out'),
      )
    except: ...
    print(".", end="", flush=True)
    clean_imgs()
  print("Done!")

def main(args):
    image_dir = os.path.abspath(args.data_loc)
    if not args.num_images:
      print("Must pass num_images")
      exit()
    n = int(args.num_images)
    if not args.bundler:
      print("Must pass loc of bundle.xml")
      exit()

    bundle_loc = os.path.abspath(args.bundler)
    create_bundles(bundle_loc, image_dir, n)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_loc", help="path to folder containing the reconstruction images", default="data/ET")
    parser.add_argument("--bundler", help="loc of bundle.xml")
    parser.add_argument("--num_images", help="first k images to process in the list.txt file")
    args = parser.parse_args()
    main(args)
