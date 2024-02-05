%% Get MRI mesh from .mri or .nii file
clear all
clc
% Fieldtrip path
addpath('/d/mjt/s4/toolboxes/fieldtrip/fieldtrip-20220214')
ft_defaults


% set project folder
project_dir = '/d/mjt/9/projects/OPM/';

% set data folder
data_dir = [project_dir,'/Coregistration Material'];
cd(data_dir) % cd to directory

%% Load in MRI
[mri_file,mri_path] = uigetfile('*.nii'); % pick MRI nifty
mri_orig = ft_read_mri([mri_path mri_file]); % read in MRI

%% Segment using FieldTrip 
cfg = [];
cfg.output    = {'brain' 'scalp'};
cfg.scalpsmooth = 25;
cfg.scalpthreshold = 0.05;
%cfg.brainthreshold = 0.40;
segmentedmri  = ft_volumesegment(cfg, mri_orig); % segment MRI
disp('Done!')

cfg = [];cfg.tissue = {'brain' 'scalp'};
cfg.numvertices = [5000 5000 5000];
mesh2 = ft_prepare_mesh(cfg,segmentedmri); % get meshes
mesh1 = ft_convert_units(mesh2,'m');

% create meshes variable
for n = 1:size(mesh1,2)
    meshes(n).pnt = mesh1(n).pos;
    meshes(n).tri = mesh1(n).tri;
    meshes(n).unit = mesh1(n).unit;
    meshes(n).name = cfg.tissue{n};
end

% plot meshes - check this looks OK. If it does not, change scalpthreshold
% and scalpsmooth on lines 22/23
figure;ft_plot_mesh(meshes,'facecolor',[.5 .5 .5],'facealpha',.3,'edgecolor','none')

%% Turn template MR scalp into a pointcloud
plypts = meshes(2).pnt;
plycolour = repmat([0.5 0.5 0.5],length(plypts),1);
meshptc = pointCloud(plypts,'Color',plycolour);
% plot to check
pcshow(meshptc)

%% Save scalp pointcloud 
% save scalp pointcloud
%pcwrite(meshptc,[data_dir '/' mri_file(1:end-4) '_scalp_points.ply'],'PLYformat','binary');
pcwrite(meshptc,[mri_path mri_file(1:end-4) '_scalp_points.ply'],'PLYformat','binary');