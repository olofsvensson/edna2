import sys
import h5py
import numpy
import tempfile
import pathlib
import matplotlib
import matplotlib.pyplot as plt

def createColourMap():
    cdict = {
        "red": (
            (0.0, 0.0, 0.0),
            (0.4, 1.0, 1.0),
            (0.6, 1.0, 1.0),
            (0.8, 1.0, 1.0),
            (1.0, 1.0, 1.0),
        ),
        "green": (
            (0.0, 0.0, 0.0),
            (0.4, 0.0, 0.0),
            (0.6, 0.4, 0.4),
            (0.8, 0.7, 0.7),
            (1.0, 1.0, 1.0),
        ),
        "blue": (
            (0.0, 0.0, 0.0),
            (0.4, 0.0, 0.0),
            (0.6, 0.0, 0.0),
            (0.8, 0.1, 0.1),
            (1.0, 0.3, 0.3),
        ),
    }
    return matplotlib.colors.LinearSegmentedColormap("my_colormap", cdict, N=256)

# ncols = 400
# nrows = 600
# raw_data_path = pathlib.Path("/data/visitor/mx2545/id29/20231206/RAW_DATA/TLN_apo/TLN_apo/run_0")


ncols = 380
nrows = 600
data_path = "/data/visitor/mx2545/id29/20231128/RAW_DATA/Mpro_WT_tr/Mpro_WT_60sec-msp4-5/run_5/aggregated/master_Mpro_WT_tr-Mpro_WT_tr_dense.h5"
raw_data_path = pathlib.Path("/data/visitor/mx2545/id29/20231128/RAW_DATA/Mpro_WT_tr/Mpro_WT_60sec-msp4-5/run_5")

print(raw_data_path)

aggregated_path = raw_data_path / "aggregated"
list_h5_path= list(aggregated_path.glob("*.h5"))
first_path = list_h5_path[0]
first_file_name = first_path.name
print(first_file_name)
prefix = "_".join(first_file_name.split("_")[0:-1])
print(prefix)
data_path = aggregated_path / (prefix + ".h5")
print(data_path)
print(data_path.exists())

f = h5py.File(data_path, "r")
isHit = f["/entry_0000/processing/peakfinder/nPeaks"][()]

tmp_14_days_path = pathlib.Path("/tmp_14_days")
opid29_path = tmp_14_days_path / "svensson"
if not opid29_path.exists():
    opid29_path.mkdir(mode=0o755)
result_dir = pathlib.Path(tempfile.mkdtemp(prefix=prefix + "_", dir=opid29_path))
result_dir.chmod(0o755)
result_path = result_dir / "mesh_plot.png"
result_hdf5_path = result_dir / "mesh_plot.h5"

isHit.shape = (nrows, ncols)
cmap = createColourMap()
matplotlib.cm.register_cmap(name="hotmodify", cmap=cmap)
isHit = numpy.clip(isHit, 0, 10)
imgplot = plt.imshow(isHit, interpolation="none")
imgplot.set_cmap("hotmodify")
plt.colorbar(orientation="vertical", shrink=0.75, pad=0.1)
plt.savefig(result_path)
print(result_path)
plt.show()

f = h5py.File(result_hdf5_path, "w")
dset = f.create_dataset("nPeaks", isHit.shape, dtype=isHit.dtype)
f.close()
print(result_hdf5_path)

#
# t0 = time.time()
# f = h5py.File(data_path, "r")
# isHit = f["/entry_0000/processing/peakfinder/isHit"][()]
# t1 = time.time()
# print(round(t1-t0,1))
# print(f"No data points : {len(isHit)}")
# print(f"Type of data   : {type(isHit)}")
# print(f"Max value      : {max(isHit)}")
# print(f"Min value      : {min(isHit)}")
#
# isHit.shape = (nrows, ncols)
# print(isHit.shape)
# plt.imshow(isHit, interpolation="none")
# plt.show()
