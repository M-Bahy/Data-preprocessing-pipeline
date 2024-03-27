import os
import shutil
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
from concurrent.futures import ProcessPoolExecutor

load_dotenv()
Parent_Directory = os.getenv("Parent_Directory")
Output_Directory = os.getenv("Output_Directory")
CloudComPy310_path = os.getenv("CloudComPy310_path")
Filter_script_path = os.getenv("Filter_script_path")
Script_name = Filter_script_path.split("\\")[-1]
Filter = os.getenv("Filter") == "True"
sub_directories = [
    d
    for d in os.listdir(Parent_Directory)
    if os.path.isdir(os.path.join(Parent_Directory, d))
]


def scan_sub_directory(sub_directory):
    """
    Scans the given sub-directory for CSV files and returns the recording file name and a list of CSV file names.

    Args:
        sub_directory (str): The name of the sub-directory to scan.

    Returns:
        tuple: A tuple containing the recording file name (str) and a list of CSV file names (list of str).

    Raises:
        Exception: If no CSV files are found in the sub-directory.

    """
    try:
        files = os.listdir(os.path.join(Parent_Directory, sub_directory))
        csv_file_names = [file for file in files if file.endswith(".csv")]
        if not csv_file_names:
            print("Parent Directory: ", Parent_Directory)
            print("Sub Directory: ", sub_directory)
            raise Exception("CSV files not found")
        #recording_file_name = csv_file_names[0]
        print("Scanned directory successfully")
        print(f"Recording file name: {sub_directory}")
        print(f"CSV files found: {len(csv_file_names)} files")
        return sub_directory, csv_file_names
    except Exception as e:
        raise Exception(
            f"An error occurred while scanning the sub-directory {sub_directory} :", e
        )


def decode_recording_file_name(recording_file_name):
    """
    Decode the recording file name to extract the date and time.

    Args:
        recording_file_name (str): The name of the recording file.

    Returns:
        tuple: A tuple containing the date and time extracted from the recording file name.

    Raises:
        Exception: If an error occurs while decoding the recording file name.

    """
    try:
        date = recording_file_name.split(" ")[0]
        time = (
            recording_file_name.split(" ")[1].split(".")[0].replace("-", ":")
            + "."
            + recording_file_name.split(" ")[1].split(".")[1]
        )
        return date, time
    except Exception as e:
        raise Exception("An error occurred while decoding the recording file name:", e)


def output_folder_hierarchy(sub_directory, date):
    """
    Create the output folder hierarchy for storing processed data and copy the filter script to the data directory if filtering is enabled.
    The filter script runs in its own directory that is why it is copied to the data directory. and it will delete itself after filtering the data.

    Args:
        sub_directory (str): The sub-directory within the output directory.
        date (str): The date for creating a sub-directory within the output directory.

    Raises:
        Exception: If an error occurs while creating the output folder hierarchy.

    Returns:
        None
    """
    try:
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
    except Exception as e:
        raise Exception(
            "An error occurred while creating the output folder hierarchy:", e
        )


def init_pipeline(sub_directory):
    """
    Initializes the data preprocessing pipeline.

    Args:
        sub_directory (str): The path to the sub-directory containing the data.

    Returns:
        tuple: A tuple containing the recording file name, a list of CSV file names,
               the date extracted from the recording file name, and the time extracted
               from the recording file name.

    Raises:
        Exception: If an error occurs while initializing the pipeline.

    """
    try:
        recording_file_name, csv_file_names = scan_sub_directory(sub_directory)
        date, time = decode_recording_file_name(recording_file_name)
        output_folder_hierarchy(sub_directory, date)
        return recording_file_name, csv_file_names, date, time
    except Exception as e:
        raise Exception("An error occurred while initializing the pipeline:", e)


def write_time_stamp(date, time, sub_directory):
    """
    Write the given date and time to a timestamps.txt file.

    Args:
        date (str): The date to be written.
        time (str): The time to be written.
        sub_directory (str): The sub-directory where the timestamps.txt file will be created.

    Raises:
        Exception: If an error occurs while writing the timestamp.

    """
    try:
        timestamps = os.path.join(
            Output_Directory, sub_directory, date, "velodyne_points", "timestamps.txt"
        )
        with open(timestamps, "a") as f:
            f.write(f"{date} {time}\n")
    except Exception as e:
        raise Exception("An error occurred while writing the timestamp:", e)


def process_csv_files(csv_file_names, sub_directory, directory_number, date, time):
    """
    Converts CSV files in the specified sub-directory to KITTI format (X, Y, Z, intensity in a text file) and writes the timestamps in timestamps.txt file.

    Args:
        csv_file_names (list): List of CSV file names.
        sub_directory (str): Sub-directory where the CSV files are located.
        directory_number (int): Directory number.
        date (str): Date of the recording.
        time (str): Time of the frame.

    Raises:
        Exception: If CSV files are not found or an error occurs while processing the files.

    Returns:
        None
    """
    try:
        files = os.listdir(os.path.join(Parent_Directory, sub_directory))
        print("Parent Directory: ", Parent_Directory)
        print("Sub Directory: ", sub_directory)
        csv_file_names = [file for file in files if file.endswith(".csv")]
        csv_file_names.sort(
            key=lambda file: int(file.split(" ")[-1].split(".")[0][:-1])
        )
        if not csv_file_names:
            raise Exception("CSV files not found")
        for count, csv_file_name in enumerate(csv_file_names, start=0):
            print("File name: ", csv_file_name)
            csv_file_path = os.path.join(Parent_Directory, sub_directory, csv_file_name)
            data_frame = pd.read_csv(csv_file_path)
            frame_date,frame_time = decode_recording_file_name(csv_file_name)
            write_time_stamp(frame_date, frame_time, sub_directory)
            data_frame = data_frame[
                ["Points_m_XYZ:0", "Points_m_XYZ:1", "Points_m_XYZ:2", "intensity"]
            ]
            data_frame = data_frame.applymap(lambda x: f"{float(x):.8f}")
            count_str = str(count).zfill(10)
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
        print(
            f"Processed 100% of the CSV files in {sub_directory} (directory {directory_number})."
        )
        print("Processed CSV files successfully.")
    except Exception as e:
        raise Exception("An error occurred while processing the CSV files:", e)


def filter_the_data(sub_directory, date):
    """
    Filter the data using a CloudComPy SOR filter.

    Args:
        sub_directory (str): The sub-directory where the data is located.
        date (str): The date of the recording.

    Returns:
        int: 0 if the filtering process is successful.

    Raises:
        Exception: If an error occurs while filtering the data.
    """
    print(
        "It is recommended to close all other applications as the filtering process is cpu intensive."
    )
    print(
        "Don't touch the app and don't worry if it's not responding, it's working on the background. It will take a while."
    )
    try:
        # Go to the CloudComPy310 directory, activate the CloudComPy310 environment, and run the filter script.
        # Since CloudComPy310 is still in development, it can only run in a conda environment.
        os.system(
            f"cmd /k cd \"{CloudComPy310_path}\" ^&^& conda activate CloudComPy310 ^&^& envCloudComPy.bat ^&^& Python \"{os.path.join(Output_Directory,sub_directory, date, 'velodyne_points', 'data', Script_name)}\" ^&^& exit"
        )
        return 0
    except Exception as e:
        raise Exception("An error occurred while filtering the data:", e)


def convert_to_kitti_format(sub_directory, directory_number):
    """
    Converts the data in the specified sub_directory to the KITTI format.

    Args:
        sub_directory (str): The path to the sub-directory containing the data.
        directory_number (int): The directory number.

    Returns:
        int: Returns 0 if the conversion is successful.

    Raises:
        Exception: If an error occurs during the conversion process.
    """
    try:
        recording_file_name, csv_file_names, date, time = init_pipeline(sub_directory)
        process_csv_files(csv_file_names, sub_directory, directory_number, date, time)
        if Filter:
            return filter_the_data(sub_directory, date)
        return 0
    except Exception as e:
        return str(e)


def live_preprocessing(GUI):
    """
    Preprocesses the data by converting it to the KITTI format and filtering it if required. The process is parallelized using the ProcessPoolExecutor.

    Args:
        GUI: An instance of the GUI class.

    Returns:
        None
    """
    try:
        start_time = datetime.now()
        with ProcessPoolExecutor() as executor:
            results = executor.map(
                convert_to_kitti_format,
                sub_directories,
                range(1, len(sub_directories) + 1),
            )

        results = list(results)
        success = True
        for result in results:
            if result != 0:
                GUI.errorMessage("Error", result)
                print("An error occurred while processing the data.")
                success = False
                print(result)
        if success:
            GUI.infoMessage(
                "Done",
                f"Application finished successfully in {datetime.now() - start_time}",
            )
    except Exception as e:
        GUI.errorMessage("Error", e)
