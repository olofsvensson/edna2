import h5py
import time

data_path = "/data/visitor/mx2545/id29/20231128/RAW_DATA/Mpro_WT_tr/Mpro_WT_60sec-msp4-5/run_5/aggregated/master_Mpro_WT_tr-Mpro_WT_tr_dense.h5"

f = h5py.File(data_path, "r")
t0 = time.time()
isHit = f["/entry_0000/processing/peakfinder/isHit"][()]
t1 = time.time()
print(round(t1-t0,1))
