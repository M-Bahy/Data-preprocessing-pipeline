# Project Title

The data preprocessing pipeline for the Sensor Calibration and Data Collection Pipeline Bachelor Thesis Project 24' at the GUC under the supervision of Dr. Eng. Catherine M. Elias. <br/>
The script takes a pcap lidar recording and CSVs of all the frames and outputs the data in KITTI format by removing the extra columns and adding the timestamp to the point cloud data and converting the point cloud into text files.

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