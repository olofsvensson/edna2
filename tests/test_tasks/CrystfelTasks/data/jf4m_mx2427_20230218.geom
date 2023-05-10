; 
; Optimized panel offsets can be found at the end of the file

photon_energy = 11560 eV ; dependent of the experiment, can be imported from a HDF5 file
; photon_energy_bandwidth = 0.01
; adu_per_eV = 8.6505-05 ; dependent of the experiment (equal to 1 over photon energy in eV)
adu_per_photon = 478.60  ; dependent of the experiment (equal to 41.401 times photon energy in keV)

clen = 0.15007
res = 13333.3 ; 75 micron pixel size

dim0 = %
dim1 = ss
dim2 = fs
data = /entry_0000/measurement/data


rigid_group_m0 = m0
rigid_group_m1 = m1
rigid_group_m2 = m2
rigid_group_m3 = m3
rigid_group_m4 = m4
rigid_group_m5 = m5
rigid_group_m6 = m6
rigid_group_m7 = m7

rigid_group_collection_detector = m0,m1,m2,m3,m4,m5,m6,m7

m0/min_fs = 0.0
m0/min_ss = 0.0
m0/max_fs = 1029.0
m0/max_ss = 513.0
m0/fs = +0.999999x -0.001092y
m0/ss = +0.001092x +0.999999y
m0/corner_x = -1059.93
m0/corner_y = -1136.12

m1/min_fs = 1038.0
m1/min_ss = 0.0
m1/max_fs = 2067.0
m1/max_ss = 513.0
m1/fs = +0.999997x -0.002096y
m1/ss = +0.002096x +0.999997y
m1/corner_x = -20.1979
m1/corner_y = -1135.12

m2/min_fs = 0.0
m2/min_ss = 550.0
m2/max_fs = 1029.0
m2/max_ss = 1063.0
m2/fs = +1.000000x +0.000208y
m2/ss = -0.000208x +1.000000y
m2/corner_x = -1059.83
m2/corner_y = -586.322

m3/min_fs = 1038.0
m3/min_ss = 550.0
m3/max_fs = 2067.0
m3/max_ss = 1063.0
m3/fs = +0.999998x -0.002111y
m3/ss = +0.002111x +0.999998y
m3/corner_x = -21.4172
m3/corner_y = -584.567

m4/min_fs = 0.0
m4/min_ss = 1100.0
m4/max_fs = 1029.0
m4/max_ss = 1613.0
m4/fs = +0.999998x -0.001570y
m4/ss = +0.001570x +0.999998y
m4/corner_x = -1060.41
m4/corner_y = -36.3206

m5/min_fs = 1038.0
m5/min_ss = 1100.0
m5/max_fs = 2067.0
m5/max_ss = 1613.0
m5/fs = +1.000000x +0.000071y
m5/ss = -0.000071x +1.000000y
m5/corner_x = -21.6348
m5/corner_y = -35.7652

m6/min_fs = 0.0
m6/min_ss = 1650.0
m6/max_fs = 1029.0
m6/max_ss = 2163.0
m6/fs = +1.000000x +0.000767y
m6/ss = -0.000767x +1.000000y
m6/corner_x = -1059.95
m6/corner_y = 513.127

m7/min_fs = 1038.0
m7/min_ss = 1650.0
m7/max_fs = 2067.0
m7/max_ss = 2163.0
m7/fs = +1.000000x +0.000938y
m7/ss = -0.000938x +1.000000y
m7/corner_x = -20.1975
m7/corner_y = 514.234


m0/coffset = -0.000175
m1/coffset = -0.000175
m2/coffset = -0.000175
m3/coffset = -0.000175
m4/coffset = -0.000175
m5/coffset = -0.000175
m6/coffset = -0.000175
m7/coffset = -0.000175
