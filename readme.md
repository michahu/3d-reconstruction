**Running ```loss_plots.py```**
```loss_plots.py``` basically bootstraps bundler by chdir into a folder containing reconstruction images, creating a bundler configuration file on the fly, and running bundler on a growing list of images. The script takes care of unzipping gzipped sift files and creating a reference ```gold.out``` bundle from all the images in a sequence if it doesn't already exist.
1. Create a data folder somewhere in the repo and make sure it's untracked by git.
2. Run ```python loss_plots.py --data_loc <rel/path/to/data> --bundler_loc <rel/path/to/RunBundler.sh> --start_idx <i> --end_idx <j> --step <k>```, making sure that ```<i>``` and ```<j>``` are within bounds of the images listed in ```list.txt```.
3. Optionally run with ```--to_npz``` to save the losses to a zipped npz.

**Reading a bundler outfile:**

https://www.cs.cornell.edu/~snavely/bundler/bundler-v0.4-manual.html


**Bundler Installation and Running Bash Program Steps for Linux**

1. ```git clone https://github.com/snavely/bundler_sfm.git```
2. Visit http://www.cs.cornell.edu/~snavely/bundler/ and Bundler Version 0.4. 
3. After unzipping the download, copy the ```jhead``` file (just ```jhead```, not ```jhead.exe``` unless you're on Windows) to the bundler ```bin``` folder.
4. Visit http://www.cs.ubc.ca/~lowe/keypoints/
 and click the "SIFT demo program (Version 4, July 2005)" link to download a ZIP containing the SIFT binary. 
5. Unzip and copy the ```sift``` file to your bundler ```bin``` folder.
6. Install ImageMagick: ```sudo apt install imagemagick```. 
7. Do this: ```sudo apt-get install libc6-dev-i386``` as per https://github.com/snavely/bundler_sfm/issues/36.
8. Install the correct matrix libraries: ```sudo apt-get install libblas-dev``` as per https://github.com/snavely/bundler_sfm/issues/21. You may have to run ```sudo apt-get autoremove libblas3``` and ```sudo apt-get autoremove libopenblas-base``` first.
9. Install FORTRAN compiler: ```sudo apt-get install gfortran```.
10. In bashrc or bash_profile, add the following line: ```export LD_LIBRARY_PATH="/path/to/bundler/bin"```. For instance, I added ```export LD_LIBRARY_PATH="/home/justiny/Documents/Princeton/Courses/COS429/Project/bundler_sfm/bin"```
11.  Navigate to bundler directory and ```make```.
12. Check to see that everything works by navigating to one of the example directories (e.g. ```/path/to/bundler/examples/kermit```) and calling the bash program: ```bash ../../RunBundler.sh```. If everything works, you should see a populated ```bundler.out``` file in the ```kermit/bundle``` folder

There's also a Python script that is supposed to do the same thing but I haven't played around with it yet.

**Debugging**

- cannot execute 'f951' --> means you don't have fortran compiler installed.
- for Arch users: ```sudo pacman -S blas lapack``` before doing any of the steps above

@Julian I just found this: http://openendedgroup.com/field/ReconstructionDistribution which might be easier for MacOS.


Camera PCA for SfM Generated Images

What is [SfM](https://en.wikipedia.org/wiki/Structure_from_motion)?



Resources for constructing objects from collections of cameras:

- [Robust Global Translations with 1DSfM](http://www.cs.cornell.edu/projects/1dsfm/)

Bundler seems to be one of the original tools for SfM.
- [Structure from Motion (SfM) for Unordered Image
Collections](http://www.cs.cornell.edu/~snavely/bundler/)

Resources for point cloud loss computation:

Need to compute some minimal matching from all points in new to points in old point
cloud(original with all cameras retained). Generally, we expect there to be fewer points in new
than in old, and the ordering returned to us might not be the same on different runs of the
algorithm.

Relevant Papers
- [Scene Reconstruction and Visualization from Internet Photo Collections: A Survey](https://www.jstage.jst.go.jp/article/ipsjtcva/3/0/3_0_44/_article/-char/ja/)
- [Modeling the World from Internet Photo Collections](http://phototour.cs.washington.edu/ModelingTheWorld_ijcv07.pdf)
- [Rapid 3D Reconstruction for Image Sequence Acquired from UAV Camera](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5795716/)
- [Weight Loss for Point Clouds
Classification](https://iopscience.iop.org/article/10.1088/1742-6596/1229/1/012045/pdf)
- [CS468: 3D Deep Learning
on Point Cloud
Data](http://graphics.stanford.edu/courses/cs468-17-spring/LectureSlides/L14%20-%203d%20deep%20learning%20on%20point%20cloud%20representation%20(analysis).pdf)
- [Multi-image 3D reconstruction data evaluation](https://www.sciencedirect.com/science/article/abs/pii/S1296207412001926)
- [Network Principles for SfM:
Disambiguating Repeated Structures with Local Context](https://www.cv-foundation.org/openaccess/content_iccv_2013/papers/Wilson_Network_Principles_for_2013_ICCV_paper.pdf)
