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
