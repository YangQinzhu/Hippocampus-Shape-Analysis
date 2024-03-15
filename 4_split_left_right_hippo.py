"""
split_left_right_and_registrate

aimed to split_left_right hippocampus first

"""

import trimesh
import numpy as np
import copy 
import open3d as o3d
import copy
import glob
import os

def split_left_right(input_mesh_path, right_path, left_path):
    """
    split left and right hippo for fine tuning
    """    

    mesh = trimesh.load_mesh(input_mesh_path)
    print(mesh.euler_number)
    mesh_connect_components = trimesh.graph.connected_components(mesh.face_adjacency)
    
    if len(mesh_connect_components) > 1:
            total_volume = mesh.volume
            print(total_volume)
    
    # split left and right
    for i in range(len(mesh_connect_components)):
        component = mesh_connect_components[i]
        submesh = copy.deepcopy(mesh)
        mask = np.zeros(len(mesh.faces), dtype=np.bool_)
        mask[component] = True
        submesh.update_faces(mask)
 
        if submesh.centroid[0] < mesh.centroid[0]:
            X = np.where(mesh.vertices[:,0] < mesh.centroid[0])
            mask_vertices = np.zeros(len(mesh.vertices), dtype=np.bool_)
            mask_vertices[X[0]] = True
            
            saved_path = right_path
            
        elif submesh.centroid[0] >= mesh.centroid[0]:
            X = np.where(mesh.vertices[:,0] >= mesh.centroid[0])
            mask_vertices = np.zeros(len(mesh.vertices), dtype=np.bool_)
            mask_vertices[X[0]] = True
            
            saved_path = left_path
        
        submesh.update_vertices(mask_vertices)
        result = trimesh.exchange.ply.export_ply(submesh)  
            
        output_file = open(saved_path, "wb+")
        output_file.write(result)
        output_file.close()

def main_process():
    mesh_dir = "./output_data/sr_registrated_cpd_mesh"
    all_mesh = glob.glob(mesh_dir + "/*.ply")
    all_mesh.sort()
    
    output_split_l_r_dir = "./output_data/sr_registrated_cpd_mesh_split_l-r"
    for i in all_mesh:
        print(i)
        
        input_mesh_path = i
        output_right_path = input_mesh_path.replace(mesh_dir, output_split_l_r_dir).replace(".ply", "_right.ply")
        output_left_path = input_mesh_path.replace(mesh_dir, output_split_l_r_dir).replace(".ply", "_left.ply")
        
        print(output_right_path, output_left_path)

        father_dir = os.path.dirname(output_right_path)
        if not os.path.exists(father_dir):
            os.makedirs(father_dir)
            
        split_left_right(input_mesh_path, output_right_path, output_left_path)
        
if __name__ == "__main__":
    main_process()