import numpy as np
import open3d as o3d
import seaborn as sns
import webcolors
import argparse

def main(args):
    sns.set()
    sns.set_palette('dark')
    pcd = o3d.io.read_point_cloud(args.input_file)
    downpcd = pcd.voxel_down_sample(voxel_size=0.05)
    print(webcolors.hex_to_rgb(sns.xkcd_rgb['indigo']))
    r, g, b = webcolors.hex_to_rgb(sns.xkcd_rgb['indigo'])
    downpcd.paint_uniform_color([r / 255, g / 255, b / 255])
    o3d.visualization.draw_geometries([downpcd])

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', help='ply file to visualize')
    args = parser.parse_args()
    main(args)