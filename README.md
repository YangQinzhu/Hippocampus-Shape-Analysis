# Fine hippocampal morphology analysis with a multi-dataset cross-sectional study on 2911 subjects
This repository contains the process code of registration and mesh conversion.

## Mesh conversion
1. Install Slicer software;
2. Write the output dir path and the suffix of the input segmentation files
3. run the following code in terminal:
```
Slicer --python-script genVTKFromBinary.py --no-splash --testing
``` 

## Registration
1. Please change the `sr_ply_dir`, `registrated_ply_dir` and `target_pd_path` to your own path first. And then run the `main.py`.

## Acknowledgement
The code is mostly based on the 3D Slicer, open3d, probreg software. Thanks for their contribution.