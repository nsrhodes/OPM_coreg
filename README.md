# OPM_coreg
Pipeline for OPM coregistration using MRI anatomy and 3D printed helmets to get array geometry

Software needed:
- Matlab
- FieldTrip
- MeshLab https://www.meshlab.net/ 
- Python with PyMeshlab package installed in environment https://pymeshlab.readthedocs.io/en/latest/

Data needed:
- Anatomical MRI (.nii)
- Einscan of participant wearing helmet (saved as .ply or .stl) [referred to as 'HNF']
- .stl/.ply of helmet used
- Locations and orientations of sensors in the corresponding helmet (for later analysis)

Get mesh of scalp from MRI (get .ply from .nii):
Run 'get_mri_mesh.m', ensuring correct paths for fieldtrip and project directory
Select '.nii' for MRI 
A figure will come up
In the command window type y, press enter then type:
r (press enter), a (press enter), s (press enter), n (press enter)
This should then segment the MRI (takes a few minutes) and plot the point cloud of scalp points

Run 'coregistration_meshlab.py' ensuring correct paths and PyMeshlab installed
Select the Einscan with the participant wearing the helmet
Select the scalp points file made from the get_mri_mesh script
Select the helmet file used
Meshlab will open with all three loaded in and the scalp points converted to a mesh
Ensure scalp points mesh is light grey and you can see features, otherwise you need to invert the faces’ orientations on filters, normal curvatures and orientation, invert faces orientation. Click apply and then close. 
Select the scalp points 'Poisson mesh' and click the 'A' button to align
With Poisson mesh highlighted, select 'glue here mesh'
Click on the Einscan and select 'point based gluing'
Select corresponding features by double clicking on the corresponding points in meshes
Select OK when you have at least 4 features
Repeat this with the Einscan 'glued' and the helmet file as 'point based gluing'
Save the project
Close the project
Select the project in the options box
Check that the transformation file saved out contains a 4x4 matrix
