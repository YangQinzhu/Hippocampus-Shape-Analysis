"""
cut out the dentation area from the registrated hippocampal point cloud

1. use color to record segmentation point
2. use kdtree to accelerate search
3. use multiprocessing for data process

"""
import os
from multiprocessing import Pool
import glob
import os
import open3d as o3d
import transforms3d as trans
from probreg import cpd
from probreg import callbacks
# import utils
import datetime
import transforms3d as t3d
import copy
import numpy as np

def cal_the_min_distance_point_use_color(zip_para):
    """
    find out the shortest distance to point cloud first and
    check whether the point is in the dentation area

    Returns:
        _type_: _description_
    """    
    (this_mesh_path, mesh_with_label_path, output_color_path) = zip_para
    print(this_mesh_path, mesh_with_label_path, output_color_path)

    start = datetime.datetime.now()
    
    this_pc = o3d.io.read_point_cloud(this_mesh_path)
    pcd_with_label_pc = o3d.io.read_point_cloud(mesh_with_label_path) 
    
    this_pc_arr = np.asarray(this_pc.points)
    first_pc_arr = np.asarray(pcd_with_label_pc.points)
    
    this_pc_color = np.zeros_like(this_pc_arr)  
    
    # set the color for the point cloud
    # this_pc_color =+ 0.588
    
    first_pc_color = np.asarray(pcd_with_label_pc.colors)

    print("find....")
    
    red_index_in_this_pc = []
    for i in range(len(this_pc_arr)):
        now_this_p = this_pc_arr[i]

        # use KDTree to find point
        now_this_p_reshape = np.reshape(now_this_p, (1, 3))
        new_arr_add_i_point = np.concatenate((first_pc_arr, now_this_p_reshape), axis=0)
        pcd_add_i_point = o3d.geometry.PointCloud()
        pcd_add_i_point.points = o3d.utility.Vector3dVector(new_arr_add_i_point)
        pcd_tree = o3d.geometry.KDTreeFlann(pcd_add_i_point)
        [k, idx, _] = pcd_tree.search_knn_vector_3d(pcd_add_i_point.points[-1], 2) # include this 

        min_j_index = idx[1]
        if first_pc_color[min_j_index, 0] == 1:
            this_pc_color[i, 0] = 1
            red_index_in_this_pc.append(i)
                
    print("find done!")
    end = datetime.datetime.now()
    print (end - start)
    
    # saved in mesh
    mesh = o3d.io.read_triangle_mesh(this_mesh_path)

    mesh.vertex_colors = o3d.utility.Vector3dVector(this_pc_color)
    o3d.io.write_triangle_mesh(output_color_path, mesh)
    
    return red_index_in_this_pc

def seg_point_use_color_KDTree_multiprocess():
    
    reg_sr_mesh_dir = "./output_data/sr_registrated_cpd_mesh_split_l-r_regFT"
    all_ply = glob.glob(reg_sr_mesh_dir + "/*.ply")
    all_ply.sort()
    
    # just for test
    # all_ply = all_ply[:2]
    
    output_mesh_with_color_dent_dir = "./output_data/sr_registrated_cpd_mesh_split_l-r_regFT_withColDent"
    
    cmd_list = []
    
    # left-right
    fix_left_path = "./source_data/target_ply/ADNI2_M3_ADNI_002_S_5018_MR_MPRAGE_br_raw_20130211111809293_100_S181892_I358618_reg_mesh_left.ply"
    fix_right_path = "./source_data/target_ply/ADNI2_M3_ADNI_002_S_5018_MR_MPRAGE_br_raw_20130211111809293_100_S181892_I358618_reg_mesh_right.ply"
    
    
    for i in range(len(all_ply)): 
        
        this_mesh_path = all_ply[i]
        print(this_mesh_path)
        
        output_color_path = this_mesh_path.replace(reg_sr_mesh_dir, output_mesh_with_color_dent_dir).replace(".ply", "_withColDent.ply")
        father_dir = os.path.dirname(output_color_path)
        if not os.path.exists(father_dir):
            os.makedirs(father_dir)
        
        # use label name
        basename = os.path.basename(this_mesh_path)
        if "_left.ply" in basename:
            mesh_with_label_path = fix_left_path
        elif "_right.ply" in basename:
            mesh_with_label_path = fix_right_path
            
        # throw out nonexistent file
        else:
            mesh_with_label_path = None
        
        cmd_list.append((this_mesh_path, mesh_with_label_path, output_color_path))
    
    print(cmd_list)
    # cmd_list.sort()
    # max process
    pool=Pool(processes=32) 
    
    pool.map(cal_the_min_distance_point_use_color, cmd_list)        
    pool.close()
    pool.join()

if __name__ == "__main__":
    seg_point_use_color_KDTree_multiprocess()
    