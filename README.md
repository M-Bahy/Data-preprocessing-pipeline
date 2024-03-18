# Data Preprocessing Pipeline

Part of the Sensor Calibration and Data Collection Pipeline Bachelor Thesis Project 24' at the GUC under the supervision of Dr. Eng. Catherine M. Elias. <br/>
The script takes a directory containing n sub-directories containing CSVs of point cloud frames recorded with Velodyne's lidars and outputs the data in KITTI format and apply SOR filter on all the frames.

## Requirements

```
pip install -r requirements.txt
```
<h3 align="center">CloudCompare</h3>
<p align="center">
    <a href="https://www.danielgm.net/cc/">
        <img src="https://res.cloudinary.com/canonical/image/fetch/f_auto,q_auto,fl_sanitize,w_60,h_60/https://dashboard.snapcraft.io/site_media/appmedia/2017/02/icon_19.png" width="200" height="200" />
    </a>
</p>
<h3 align="center">Veloview</h3>
<p align="center">
    <a href="https://www.paraview.org/veloview/#download">
        <img src="https://raw.githubusercontent.com/Kitware/VeloView/master/Application/Icons/logo.png" width="200" height="200" />
    </a>
</p>
<h3 align="center">CloudComPy</h3>
<details>
    <summary>Windows</summary>
    
Installing, testing and using a CloudComPy binary on Windows 10 or 11, with Conda

The binary *CloudComPy\*_-date-.7z* available [here](https://www.simulation.openfields.fr/index.php/cloudcompy-downloads) is built in a Conda environment.
(see [here](BuildWindowsConda.md) for the corresponding building instructions).

As CloudComPy is under development, these instructions and the link are subject to change from time to time...

**This binary works only on Windows 10 or 11, and with a Conda environment as described below, not anywhere else!**

You need a recent installation of Anaconda3 or miniconda3.

You need to create a conda environment for CloudComPy: for instance, in Anaconda3, use the Anaconda3 prompt console:

```
conda activate
conda update -y -n base -c defaults conda
```
If your environment CloudComPy310 does not exist:
```
conda create --name CloudComPy310 python=3.10
   # --- erase previous env with the same name if existing
```
Add or update the packages:
```
conda activate CloudComPy310
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install "boost=1.74" "cgal=5.4" cmake draco ffmpeg "gdal=3.5" jupyterlab laszip "matplotlib=3.5" "mysql=8.0" "numpy=1.22" "opencv=4.5" "openmp=8.0" "pcl=1.12" "pdal=2.4" "psutil=5.9" pybind11 "qhull=2020.2" "qt=5.15.4" "scipy=1.8" sphinx_rtd_theme spyder tbb tbb-devel "xerces-c=3.2"
```

Install the binary in the directory of your choice.
</details>
<details>
    <summary>Linux</summary>
    
    This is the content inside the collapsible section. You can put anything you want here, including Markdown or HTML code.
</details>
<details>
    <summary>Mac</summary>
    
    This is the content inside the collapsible section. You can put anything you want here, including Markdown or HTML code.
</details>

## Installation

Provide steps on how to install the project locally.

```
git clone https://github.com/M-Bahy/Data-preprocessing-pipeline.git
cd Data-preprocessing-pipeline
```

## Environment Variables

To run this project, you will need to create your .env file

`Working_Directory` - Path to the directory containing the pcap file and the csv files

`FPS` - Frames per second of the recording

`Output_Directory` - Path to the directory where the output files will be saved in the kitti style

## Run

Use the `run.bat` to run the project or alternatively run the following commands in the terminal

```
python post_veloview.py
```

## Contributing

Contributions are always welcome! feel free to open a pull request or contact me for any changes.

## License

[MIT](https://choosealicense.com/licenses/mit/)