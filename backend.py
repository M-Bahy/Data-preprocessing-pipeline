import os
import shutil
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ProcessPoolExecutor

Parent_Directory = ""
Output_Directory = ""
CloudComPy310_path = ""
Filter_script_path = ""
Script_name = ""
offset = ""
Filter = ""
GUI = ""
sub_directories = [
    d
    for d in os.listdir(Parent_Directory)
    if os.path.isdir(os.path.join(Parent_Directory, d))
]


def scan_sub_directory(sub_directory):
    """
    Scans the directory for CSV files.
    Raises:
        Exception: If no CSV files are found in the directory.
    """
    files = os.listdir(os.path.join(Parent_Directory, sub_directory))
    csv_file_names = [file for file in files if file.endswith(".csv")]
    if not csv_file_names:
        raise Exception("CSV files not found")
    recording_file_name = csv_file_names[0].split(" ")[0]
    print("Scanned directory successfully")
    print(f"Recording file name: {recording_file_name}")
    print(f"CSV files found: {len(csv_file_names)} files")
    return recording_file_name, csv_file_names


def decode_recording_file_name(recording_file_name):
    """
    Extracts the data from the recording file name.
    """
    datetime = recording_file_name.split("_")[0]
    date = f"{datetime[:4]}-{datetime[5:7]}-{datetime[8:10]}"
    time = f"{datetime[11:13]}:{datetime[14:16]}:{datetime[17:19]}.000000"
    print("Decoded recording file name successfully")
    return date, time


def output_folder_hierarchy(sub_directory, date):
    """
    Creates a folder hierarchy for storing output files.
    """
    output_dir = os.path.join(Output_Directory, sub_directory, date)
    os.makedirs(output_dir, exist_ok=True)
    velodyne_dir = os.path.join(output_dir, "velodyne_points")
    os.makedirs(velodyne_dir, exist_ok=True)
    timestamps = os.path.join(velodyne_dir, "timestamps.txt")
    with open(timestamps, "w") as f:
        pass
    data_dir = os.path.join(velodyne_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    if Filter:
        shutil.copy(Filter_script_path, data_dir)
    print("Output folder hierarchy created successfully.")


def init_pipeline(sub_directory):
    """
    Initializes the data preprocessing pipeline.
    """
    recording_file_name, csv_file_names = scan_sub_directory(sub_directory)
    date, time = decode_recording_file_name(recording_file_name)
    output_folder_hierarchy(sub_directory, date)
    return recording_file_name, csv_file_names, date, time


def add_offset(date, time):
    """
    Adds an offset to the global date and time variables.

    This function combines the global `date` and `time` variables into a single datetime object,
    then adds the offset (in microseconds) to the datetime object. The updated date and time are
    stored back into the global variables.

    Args:
        None

    Returns:
        None
    """
    daytime = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S.%f")
    offset_seconds = offset / 1e6
    daytime += timedelta(seconds=offset_seconds)
    date, time = daytime.strftime("%Y-%m-%d"), daytime.strftime("%H:%M:%S.%f")
    return date, time


def write_time_stamp(date, time, sub_directory):
    """
    Write the date and time to a timestamps file.

    Args:
        date (str): The date in the format "YYYY-MM-DD".
        time (str): The time in the format "HH:MM:SS.mmmmmm".

    Returns:
        None
    """
    timestamps = os.path.join(
        Output_Directory, sub_directory, date, "velodyne_points", "timestamps.txt"
    )
    with open(timestamps, "a") as f:
        f.write(f"{date} {time}\n")


def process_csv_files(csv_file_names, sub_directory, directory_number, date, time):
    """
    Process CSV files in the sub_directory and convert them to TXT files.

    This function reads each CSV file in the sub_directory, applies optional data filtering,
    converts the columns to a specific format (x y z intensity), and saves the resulting data as TXT files,
    In the output directory. The function also writes the timestamps of the TXT files to a timestamps file.
    Each timestamp is written in the format "YYYY-MM-DD HH:MM:SS.mmmmmm" and represents the time of the
    corresponding TXT file.

    Raises:
        Exception: If no CSV files are found in the sub_directory.

    Returns:
        None
    """
    files = os.listdir(os.path.join(Parent_Directory, sub_directory))
    csv_file_names = [file for file in files if file.endswith(".csv")]
    csv_file_names.sort(key=lambda file: int(file.split(" ")[-1].split(".")[0][:-1]))
    if not csv_file_names:
        raise Exception("CSV files not found")
    for count, csv_file_name in enumerate(csv_file_names, start=0):
        csv_file_path = os.path.join(Parent_Directory, sub_directory, csv_file_name)
        data_frame = pd.read_csv(csv_file_path)
        if csv_file_name != csv_file_names[0]:
            add_offset(date, time)
        write_time_stamp(date, time, sub_directory)
        data_frame = data_frame[
            ["Points_m_XYZ:0", "Points_m_XYZ:1", "Points_m_XYZ:2", "intensity"]
        ]
        data_frame = data_frame.applymap(lambda x: f"{float(x):.8f}")
        count_str = str(count).zfill(6)
        txt_path = os.path.join(
            Output_Directory,
            sub_directory,
            date,
            "velodyne_points",
            "data",
            f"{count_str}.txt",
        )
        data_frame.to_csv(txt_path, sep=" ", header=False, index=False)
        if count % 10 == 0:
            percentage = (count / len(csv_file_names)) * 100
            print(
                f"Processed {percentage:.2f}% of the CSV files in {sub_directory} (directory {directory_number})."
            )
    print(f"Processed 100% of the CSV files in {sub_directory} (directory {directory_number}).")
    print("Processed CSV files successfully.")


def filter_the_data(sub_directory, date):
    """
    Filter the data using the CloudComPy library.
    """
    os.system(f"start cmd /k cd \"{CloudComPy310_path}\" ^&^& conda activate CloudComPy310 ^&^& envCloudComPy.bat ^&^& Python \"{os.path.join(Output_Directory,sub_directory, date, 'velodyne_points', 'data', Script_name)}\" ^&^& exit")
    print("Filtered the data successfully.")


def convert_to_kitti_format(sub_directory, directory_number):
    recording_file_name, csv_file_names, date, time = init_pipeline(sub_directory)
    process_csv_files(csv_file_names, sub_directory, directory_number, date, time)
    if Filter:
        filter_the_data(sub_directory, date)


def preprocessing(pyqt_instance):
    global GUI,Parent_Directory, Output_Directory, CloudComPy310_path, Filter_script_path,  offset, Filter , Script_name
    GUI = pyqt_instance
    Parent_Directory = GUI.parent_label.text()
    CloudComPy310_path = GUI.CloudComPy_label.text()
    if CloudComPy310_path.split(":")[0] == "D":
        CloudComPy310_path = "/d " + CloudComPy310_path
    Output_Directory = GUI.out_label.text()
    Filter_script_path = GUI.filter_label.text()
    offset = 1 / int(GUI.frames.text()) * 1000000
    Filter = GUI.checkBox.isChecked()
    Script_name = Filter_script_path.split("\\")[-1]
    print("Application started.")
    start_time = datetime.now()
    with ProcessPoolExecutor() as executor:
        executor.map(
            convert_to_kitti_format, sub_directories, range(1, len(sub_directories) + 1)
        )
    end_time = datetime.now()
    print(f"Time taken to process the data: {end_time - start_time}")
    print("Application finished successfully.")

