# Data Preprocessing Pipeline

Part of the Sensor Calibration and Data Collection Pipeline Bachelor Thesis Project 24' at the GUC under the supervision of Dr. Eng. Catherine M. Elias. <br/>
The script takes a directory containing n sub-directories containing CSVs of point cloud frames recorded with Velodyne's lidars and outputs the data in KITTI format and apply SOR filter on all the frames.

:warning: **This project have only been tested on Windows 10.**

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
    
Installing, testing and using a CloudComPy binary on Linux, with conda

The binary *CloudComPy_Conda310_Linux64_-date-.tgz* available [here](https://www.simulation.openfields.fr/index.php/cloudcompy-downloads) is built with a Conda environment
(see [here](BuildLinuxConda.md) for the corresponding building instructions).

As CloudComPy is under development, these instructions and the link are subject to change from time to time...

**This binary works only on Linux 64, on recent distributions, and with a Conda environment as described below, not anywhere else!**

**Only tested un Ubuntu 20.04 (focal) and Debian 11 (bullseye), please report any problems on other distributions.**

GLIBC version should be 2.29 or more. To know your version of GLIBC:

```
ldd --version
```

You need a recent installation of Anaconda3 or miniconda3.

You need to create an environment for CloudComPy with conda, from the terminal
(here, I chose to activate conda environment on demand: please adapt the instructions to your installation):

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

**Remark:** if conda is unknown, or in a bash script, add the following instruction before conda commands:

```
. <conda_dir>/etc/profile.d/conda.sh
```
where `<conda_dir>` is the installation directory of conda (often `~/anaconda3` or `~/miniconda3`)

Install the binary in the directory of your choice.
</details>
<details>
    <summary>Mac</summary>
    
Experimental: Installing, testing and using a CloudComPy binary on MacOS, with conda

The binary *CloudComPy_Conda310_MacOS-date-.zip* available [here](https://www.simulation.openfields.fr/index.php/cloudcompy-downloads)
 is built with a Conda environment.

**This binary works only on macOS Apple arm architecture (not on Intel processors), on recent macOS versions, not anywhere else!**

**Built and tested on macOS VENTURA 13.4.1. Please post issues on CloudComPy GitHub in case of problem**

The macOS binary provides **CloudCompare** and **CloudCompy** (same as binaries for Windows and Linux).

As CloudComPy is under development, these instructions and the link are subject to change from time to time...

**CloudCompare** works as it is (no specific environment).
It is located in CloudComPy310/CloudCompare/CloudCompare.app and can be launched from the Finder.

**CloudComPy** needs a Python 3.10 configuration with at least the following packages, either with conda or not:

```
numpy
scipy
requests
psutils
matplotlib
```

You can create an environment for CloudComPy with conda, from the terminal
(here, I chose to activate conda environment on demand: please adapt the instructions to your installation)
The following package list corresponds to the building environment, but you can adjust the list
(at least the above list):

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
conda install "boost" "cgal" cmake draco ffmpeg "gdal" jupyterlab laszip "matplotlib" "mysql=8.0" "numpy" "opencv" "openssl=3.0.8" "pcl" "pdal" "psutil" pybind11 "qhull=2020.2" "qt=5.15.8" "scipy" sphinx_rtd_theme spyder tbb tbb-devel "xerces-c=3.2" xorg-libx11 || error_exit "conda environment ${CONDA_ENV} cannot be completed"
```

Unzip the binary tarfile in the directory of your choice.
</details>

## Run

Use the `C-DRiVeS.bat` to run the project or alternatively run the following commands in the terminal

```
python GUI.py
```

## Prerequisite

import your Velodyne's lidar recording into [Veloview](https://www.paraview.org/veloview/#download) and choose <br/>
File -> Save As -> Save CSV -> All Frames -> OK

:warning: **The PCAP file MUST be kept with its default name**
Example:
```
2024-02-22-12-13-56_Velodyne-VLP-32C-Data.pcap
2024-03-03-16-11-09_Velodyne-Data.pcap
```

## Usage

1. Select the parent directory . Its structure should be as follows:
```
Parent_Directory
├── sub_directory_1
│   ├── recording_file_name (Frame 0).csv
│   ├── recording_file_name (Frame 1).csv
│   └── ...
├── sub_directory_2
│   ├── recording_file_name (Frame 0).csv
│   ├── recording_file_name (Frame 1).csv
│   └── ...
└── ...
```
2. Select the CloudComPy directory.
3. Select the `filter.py` file.
4. Select the output directory. Its structure will be as follows:
```
Output_Directory
├── sub_directory_1
│   └── day
│       └── velodyne_points
│           ├── timestamps.txt
│           └── data
│               └── filter.py (if filtering is enabled)
│               └── 000000.txt
│               └── 000001.txt
│               └── ...
├── sub_directory_2
│   └── day
│       └── velodyne_points
│           ├── timestamps.txt
│           └── data
│               └── filter.py (if filtering is enabled)
│               └── 000000.txt
│               └── 000001.txt
│               └── ...
├── ...
```
6. Set the recording FPS.
7. Choose whether to apply the SOR filter or not.
8. Click Start to start the process. Don't touch the window until the process is finished. It will take a while depending on your data size and your CPU. It is recommended to close all other applications as the process is CPU intensive.
It will display a message box when the process is finished.

## Contributing

Contributions are always welcome! feel free to open a pull request or contact me for any changes.

## License

[MIT](https://choosealicense.com/licenses/mit/)