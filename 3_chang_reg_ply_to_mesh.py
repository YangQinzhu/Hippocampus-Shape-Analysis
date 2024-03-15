"""
convert all pcd to mesh 

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

def convert_reg_ply_to_mesh():
    """
    ply -- mesh and output in a new dir
    change the parameter: reg_ply_dir, mesh_ply_dir, output_reg_mesh_ply_dir
    """    
    reg_ply_dir = "./output_data/sr_registrated_cpd"
    mesh_ply_dir = "./source_data"
    output_reg_mesh_ply_dir = "./output_data/sr_registrated_cpd_mesh"
    
    all_reg_ply = glob.glob(reg_ply_dir + "/*.ply")
    all_reg_ply.sort()
    
    for i in all_reg_ply:
        print(i)
        
        pcd = o3d.io.read_point_cloud(i)
        ply_arr = np.asarray(pcd.points)
        
        mesh_ply = i.replace(reg_ply_dir, mesh_ply_dir).replace("_reg.ply", ".ply")
        mesh = o3d.io.read_triangle_mesh(mesh_ply)
        mesh.vertices = o3d.utility.Vector3dVector(ply_arr)
        
        output_mesh_path = i.replace(reg_ply_dir, output_reg_mesh_ply_dir).replace("_reg.ply", "_reg_mesh.ply")
        output_mesh_father_dir = os.path.dirname(output_mesh_path)
        if not os.path.exists(output_mesh_father_dir):
            os.makedirs(output_mesh_father_dir)
                
        o3d.io.write_triangle_mesh(output_mesh_path, mesh)
    
if __name__ == "__main__":
    convert_reg_ply_to_mesh()