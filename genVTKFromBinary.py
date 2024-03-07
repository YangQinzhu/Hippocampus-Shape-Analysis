###############################################
# Convert all binary segmentation files to mesh files
###############################################

import glob
import os

def convert_binary_to_vtk(path_name, output_dir):
    print(path_name)
    # help(slicer.modules.volumes)
    volume_node = slicer.util.loadVolume(path_name, properties={"labelmap": True})
    seg_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", volume_node.GetName()+'-segmentation')
    slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(volume_node, seg_node)

    shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
    exportFolderItemId = shNode.CreateFolderItem(shNode.GetSceneItemID(), volume_node.GetName()+"-models")
    slicer.modules.segmentations.logic().ExportAllSegmentsToModels(seg_node, exportFolderItemId)

    # saved path
    saved_vtk_path = output_dir + '/' + volume_node.GetName() + '.ply'

    # Get exported model of first segment
    segmentModels = vtk.vtkCollection()
    shNode.GetDataNodesInBranch(exportFolderItemId, segmentModels)
    modelNode = segmentModels.GetItemAsObject(0)
    myStorageNode = modelNode.CreateDefaultStorageNode()
    myStorageNode.SetFileName(saved_vtk_path)
    myStorageNode.WriteData(modelNode)
    
    # delete all node, to free memory
    slicer.mrmlScene.RemoveNode(volume_node)
    slicer.mrmlScene.RemoveNode(seg_node)
    slicer.mrmlScene.RemoveNode(myStorageNode)
    slicer.mrmlScene.RemoveNode(modelNode)

def main():
    dir = "Folder containing binary files and saved output files"

    # the keyword of binary file, can be changed
    all_sr_label = glob.glob(dir+"/*_pred_binary_sr.nii.gz")
    all_sr_label.sort()
    
    for i in all_sr_label:  
        output_dir = os.path.dirname(i)
        print(i, output_dir)
        convert_binary_to_vtk(i, output_dir)
        
main()