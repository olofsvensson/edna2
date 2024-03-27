#!/opt/pxsoft/mxworkflows/id30a2/miniconda3/envs/id30a2/bin/python3.9
import os
import sys
import h5py
import numpy
import tempfile
import pathlib
import matplotlib
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser(
    description="Application for plotting nPeaks from ID29 SSX data"
)
parser._action_groups.pop()
required = parser.add_argument_group("required arguments")
optional = parser.add_argument_group("optional arguments")
required.add_argument(
    "--raw_data", action="store", help="Path to raw data", required=True
)
required.add_argument(
    "--ncols", action="store", help="Number of columns", required=True
)
required.add_argument(
    "--nrows", action="store", help="Number of rows", required=True
)
optional.add_argument(
    "--clip", action="store", help="Clipping value for plot", default=None
)
optional.add_argument(
    "--roi", action="store", help="Region of interest for plot, given as [x1, y1, x2, y2]", default=None
)

results = parser.parse_args()

raw_data_path = pathlib.Path(results.raw_data)
ncols = int(results.ncols)
nrows = int(results.nrows)
if results.roi is not None:
    roi  = eval(results.roi)
else:
    roi = None
clip = int(results.clip)vi

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

aggregated_path = raw_data_path / "aggregated"
list_h5_path= list(aggregated_path.glob("*.h5"))
first_path = list_h5_path[0]
first_file_name = first_path.name
prefix = "_".join(first_file_name.split("_")[0:-1])
data_path = aggregated_path / (prefix + ".h5")

f = h5py.File(data_path, "r")
isHit = f["/entry_0000/processing/peakfinder/nPeaks"][()]

result_dir = pathlib.Path(os.getcwd())
result_path = result_dir / "mesh_plot.png"
result_hdf5_path = result_dir / "mesh_plot.h5"

isHit.shape = (nrows, ncols)
f = h5py.File(result_hdf5_path, "w")
dset = f.create_dataset("nPeaks", isHit.shape, dtype=isHit.dtype)
f.close()
print(result_hdf5_path)

if roi is not None:
    isHit = isHit[roi[0]:roi[2], roi[1]:roi[3]]
cmap = createColourMap()
matplotlib.cm.register_cmap(name="hotmodify", cmap=cmap)
if clip is not None:
    isHit = numpy.clip(isHit, 0, clip)
imgplot = plt.imshow(isHit, interpolation="none")
imgplot.set_cmap("hotmodify")
plt.colorbar(orientation="vertical", shrink=0.75, pad=0.1)
plt.savefig(result_path)
print(result_path)
plt.show()


