#!/bin/bash

#export opt_miniconda=/home/esrf/opid29/miniconda3
#export PYTHONPATH="$HOME/progs/edna2:$opt_miniconda/lib:$opt_miniconda/lib/python3.9/site-packages"
#export HDF5_PLUGIN="$HOME/anaconda3/lib/python3.9/site-packages/hdf5plugin/plugins"
export EDNA2_SITE="ESRF_ID30A2"

python $HOME/test_edna2/edna2/bin/run_crysttask.py \
	--image_directory "/data/visitor/mx2434/id29/20230309/RAW_DATA/lysozyme_PC/lysozyme_PC/run_0" \
	--detectorType "jungfrau" --prefix "*dense" --suffix "h5" --geometry_file "/home/esrf/opid29/progs/xml_server_npc/jf4m_mx2427_20230218.geom" \
	--maxchunksize 1000 --indexing_method "xgandalf,mosflm,asdf", --partition "mx" \
        --int_radius "4,6,7" --peak_radius "4,6,7" --threshold 800 --max_res "1000"\
	--min_peaks "20" --min_snr "4.0" --num_processors "20" --local_bg_radius "5" \
        --unit_cell_file "/data/visitor/mx2434/id29/20230309/visa_demo/lyso.cell" 
