"""
multi processing for registration
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

    
def run_cmd(cmd):
    print(cmd)
    os.system(cmd)
    
def apply_registration_multi_process():

    # sr_ply_dir = "write the fold path of .ply files"
    sr_ply_dir = "./source_data"

    # registrated_ply_dir = "saved data fold"
    registrated_ply_dir = "./output_data/sr_registrated_cpd"
    
    all_ply = glob.glob(sr_ply_dir + "/*.ply")
    all_ply.sort()
    
    
    cmd_list = []
    
    # target_pd_path = "the path to referenced ply path"
    target_pd_path = "./source_data/target_ply/ADNI2_M3_ADNI_002_S_5018_MR_MPRAGE_br_raw_20130211111809293_100_S181892_I358618_pred_binary_sr.ply"
    
    print("target_pd_path:", target_pd_path)
    for i in range(len(all_ply)):
        starttime = datetime.datetime.now()
        
        source_pd_path = all_ply[i]
        print("source_pd_path:", source_pd_path)
        
        saved_path = source_pd_path.replace(sr_ply_dir, registrated_ply_dir).replace(".ply", "_reg.ply")
        father_dir = os.path.dirname(saved_path)
        if not os.path.exists(father_dir):
            os.makedirs(father_dir)
        
        # ignore this existed file 
        if os.path.exists(saved_path):
            continue
        
        # endtime = datetime.datetime.now()
        # print("end time:", endtime - starttime) 

        # change this path to registration.py
        # cmd = f"python path_to_registration.py {source_pd_path} {target_pd_path} {saved_path}"
        cmd = f"python registration.py {source_pd_path} {target_pd_path} {saved_path}"
        
        ### 
        cmd_list.append(cmd)
    
    print(len(cmd_list))
    # cmd_list.sort()

    # change this according to your process
    pool=Pool(processes=32) 
    # 
    pool.map(run_cmd, cmd_list)        
    pool.close()
    pool.join()

apply_registration_multi_process()