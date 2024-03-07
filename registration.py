"""
for registration
"""
import glob
import os
import open3d as o3d
import transforms3d as trans
from probreg import cpd
from probreg import callbacks
# import utils
import time
import transforms3d as t3d
import copy

import numpy as np
use_cuda = False

import datetime
from multiprocessing import Pool
import datetime

def reg_two_point_cloud_zipPara(source_pd_path, target_pd_path, saved_path):
    """
    return registrated point cloud
    """    
    starttime = datetime.datetime.now()
    print(source_pd_path, target_pd_path, saved_path)
    
    source_original_pcd = o3d.io.read_point_cloud(source_pd_path)
    target_original_pcd = o3d.io.read_point_cloud(target_pd_path)
    
    source = np.asarray(source_original_pcd.points, dtype=np.float32)
    target = np.asarray(target_original_pcd.points, dtype=np.float32)

    source = source[::10]
    target = target[::10]
    
    # change numpy to pointcloud
    source_pcd = o3d.geometry.PointCloud()
    source_pcd.points = o3d.utility.Vector3dVector(source)

    target_pcd = o3d.geometry.PointCloud()
    target_pcd.points = o3d.utility.Vector3dVector(target)
    
    tf_param, _, _ = cpd.registration_cpd(source_pcd, target_pcd) # default: tf_type_name = "rigid"
    
    new_source = copy.deepcopy(source_original_pcd)
    new_source.points = tf_param.transform(source_original_pcd.points)
    
    o3d.io.write_point_cloud(saved_path, new_source)
    
    endtime = datetime.datetime.now()
    print("end time:", endtime - starttime) 
        
import sys
reg_two_point_cloud_zipPara(sys.argv[1], sys.argv[2], sys.argv[3])