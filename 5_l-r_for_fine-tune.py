import trimesh
import numpy as np
import copy 
import open3d as o3d
import copy
from probreg import cpd
import datetime
import glob
import os
import shutil
from multiprocessing import Pool
    
def registrate_icp_in_trimesh_multiP(zip_param):
    fix_mesh_path, mov_mesh_path, saved_mesh_path = zip_param
    
    fix_mesh = trimesh.load(fix_mesh_path)
    mov_mesh = trimesh.load(mov_mesh_path)
    
    try:
        output_matrix, transformed, _ = trimesh.registration.icp(mov_mesh.vertices, fix_mesh.vertices)
        
        print(output_matrix)
        # print(mov_mesh.vertices.shape)
        # print(transformed.shape)
    
        mov_mesh_o3d = o3d.io.read_triangle_mesh(mov_mesh_path)
        new_mov_point = np.asarray(transformed)
        mov_mesh_o3d.vertices = o3d.utility.Vector3dVector(new_mov_point)
        o3d.io.write_triangle_mesh(saved_mesh_path, mov_mesh_o3d)
        
        # o3d.visualization.draw_geometries([mov_mesh_o3d])
    except:
        print("copy")
        shutil.copy(mov_mesh_path, saved_mesh_path)
        
def main_process():
    mesh_dir = "./output_data/sr_registrated_cpd_mesh_split_l-r"
    all_mesh = glob.glob(mesh_dir + "/*.ply")
    all_mesh.sort()
    
    # left-right
    fix_left_path = "./source_data/target_ply/ADNI2_M3_ADNI_002_S_5018_MR_MPRAGE_br_raw_20130211111809293_100_S181892_I358618_reg_mesh_left.ply"
    fix_right_path = "./source_data/target_ply/ADNI2_M3_ADNI_002_S_5018_MR_MPRAGE_br_raw_20130211111809293_100_S181892_I358618_reg_mesh_right.ply"
    
    # output
    output_l_r_reg_dir = "./output_data/sr_registrated_cpd_mesh_split_l-r_regFT"
    
    cmd_list= []
    
    for i in all_mesh:
        print(i)
        
        mov_mesh_path = i
        
        saved_mesh_path = mov_mesh_path.replace(mesh_dir, output_l_r_reg_dir)
        assert saved_mesh_path != mov_mesh_path
        
        # print(output_right_path, output_left_path)
        
        basename = os.path.basename(mov_mesh_path)
        if "_left.ply" in basename:
            fix_mesh_path = fix_left_path
        else:
            fix_mesh_path = fix_right_path
            
        father_dir = os.path.dirname(saved_mesh_path)
        if not os.path.exists(father_dir):
            os.makedirs(father_dir)

        # if os.path.exists(saved_mesh_path):
        #     continue
        
        print(fix_mesh_path, mov_mesh_path, saved_mesh_path)
        # registrate_icp_in_trimesh(fix_mesh_path, mov_mesh_path, saved_mesh_path)
        cmd_list.append((fix_mesh_path, mov_mesh_path, saved_mesh_path))
        
    cmd_list.sort()
    pool=Pool(processes=16) 
    pool.map(registrate_icp_in_trimesh_multiP, cmd_list)        
    pool.close()
    pool.join()
        
        
if __name__ == "__main__":
    main_process()
    
