# -*- coding: utf-8 -*-
"""
Created on Fri May 26 18:50:25 2023

@author: ppynr2
"""
# Housekeeping
import tkinter as tk
from tkinter.filedialog import askopenfilename
import pymeshlab
import os
import subprocess

# Set initial path and set-up tkinter for selecting files
root_path =  r'R:\DRS-KidsOPM\Paediatric_OPM_Notts\Data\BIDS\derivatives'
os.chdir(root_path)
root = tk.Tk()
root.wm_attributes("-topmost",1)
root.withdraw()

# Select hnf file
hnf_file = askopenfilename(parent=root,initialdir=root_path,title="Open HNF file")
ms = pymeshlab.MeshSet()
ms.load_new_mesh(hnf_file)
# Scale hnf file
ms.compute_matrix_from_scaling_or_normalization(axisx = 0.001, axisy = 0.001, axisz = 0.001)
path_save_helmet = hnf_file[:-4]
# Save converted file
ms.save_current_mesh(path_save_helmet + '_converted.ply', save_face_color=True)

# Select scalp file
scalp_file = askopenfilename(parent=root,initialdir=root_path,title="Open scalp points file")
ms.load_new_mesh(scalp_file)
# Compute normals
ms.compute_normal_for_point_clouds(k=8, smoothiter=100)
# Screened poisson
ms.generate_surface_reconstruction_screened_poisson(pointweight=40)
path_save_scalp = scalp_file[:-4]
# Save mesh
ms.save_current_mesh(path_save_scalp + '_mesh.ply', save_face_color=True)

# Open helmet .ply file
helmet_file = askopenfilename(parent=root,initialdir=root_path,title="Open helmet file")
ms.load_new_mesh(helmet_file)
# Save out project
ms.save_project(path_save_scalp + '_project.mlp')

# Open project in meshlab
p = subprocess.Popen(['C:\Program Files\VCG\MeshLab\meshlab.exe',path_save_scalp + '_project.mlp'])

# Conduct point-based transforms from hnf to scalp, then helmet to hnf and save project
# Then close meshlab
returncode = p.wait()

# Load project
project_file = askopenfilename(parent=root,initialdir=root_path,title="Open project file")
ms.load_project(project_file)

# Read transformation matrix
f = open(project_file,'r')
full_file = f.read()
full_file = full_file.splitlines()
tform = list()
for i in range(4):
    tform.append(full_file[i+32])
f.close()
# Write transformation matrix 
tform_file = project_file[:-24]

myfile = open(tform_file + 'sens2mri_transform.txt',mode='w',encoding='utf-8')
for item in tform:
    myfile.write(f"{item}\n")

myfile.close()
    




