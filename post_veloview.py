import os
import shutil
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
Working_Directory = os.getenv("Working_Directory")
Output_Directory = os.getenv("Output_Directory")
Cutoff_Intensity = os.getenv("Cutoff_Intensity")
offset = 1 / int(os.getenv("FPS")) * 1000000
Filter_The_Data = os.getenv("Filter_The_Data") == "True"
pcap_file_name = "2024-02-22-12-13-56_Velodyne-VLP-32C-Data"
csv_file_names = []
date = ""
time = ""


def scan_directory():
    """
    Scans the working directory for CSV and PCAP files.
    Raises:
        Exception: If no CSV files are found in the directory.
        Exception: If no PCAP file is found in the directory.
    """
    global pcap_file_name, csv_file_names
    files = os.listdir(Working_Directory)
    csv_file_names = [file for file in files if file.endswith(".csv")]
    if not csv_file_names:
        raise Exception("CSV files not found")
    pcap_files = [file for file in files if file.endswith(".pcap")]
    if not pcap_files:
        raise Exception("PCAP file not found")
    pcap_file_name = pcap_files[0]
    print("Scanned directory successfully")
    print(f"PCAP file found: {pcap_file_name}")
    print(f"CSV files found: {len(csv_file_names)} files")


def csv_folder_hierarchy():
    """
    Organizes CSV files into a directory.

    This function moves all CSV files in the working directory to a subdirectory named "VeloView CSVs" and prepare a subdirectory for CloudCompare output.

    The directory is created if it does not already exist.
    """
    csvs_dir = os.path.join(Working_Directory, "VeloView CSVs")
    os.makedirs(csvs_dir, exist_ok=True)
    cloudcompare_dir = os.path.join(Working_Directory, "CloudCompare Output")
    os.makedirs(cloudcompare_dir, exist_ok=True)
    for csv_file_name in csv_file_names:
        original_path = os.path.join(Working_Directory, csv_file_name)
        shutil.move(original_path, csvs_dir)
    print("CSV folder hierarchy created successfully.")


def decode_pcap_file_name():
    """
    Extracts the data from the PCAP file name.
    """
    global date, time
    datetime = pcap_file_name.split("_")[0]
    date = f"{datetime[:4]}-{datetime[5:7]}-{datetime[8:10]}"
    time = f"{datetime[11:13]}:{datetime[14:16]}:{datetime[17:19]}.000000"
    print("Decoded PCAP file name successfully")


def output_folder_hierarchy():
    """
    Creates a folder hierarchy for storing output files.
    """
    global date
    output_dir = os.path.join(Output_Directory, date)
    os.makedirs(output_dir, exist_ok=True)
    velodyne_dir = os.path.join(output_dir, "velodyne_points")
    os.makedirs(velodyne_dir, exist_ok=True)
    timestamps = os.path.join(velodyne_dir, "timestamps.txt")
    with open(timestamps, "w") as f:
        pass
    data_dir = os.path.join(velodyne_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    print("Output folder hierarchy created successfully.")


def create_folder_hierarchy():
    """
    Creates the folder hierarchy for the data preprocessing pipeline.
    """
    csv_folder_hierarchy()
    output_folder_hierarchy()


def init_pipeline():
    """
    Initializes the data preprocessing pipeline.
    """
    scan_directory()
    decode_pcap_file_name()
    create_folder_hierarchy()


def filter_the_data(data_frame):
    """
    Filters the data based on the intensity.
    Args:
        data_frame (pandas.DataFrame): The data frame to be filtered.
    Returns:
        pandas.DataFrame: The filtered data frame.
    """
    return data_frame[data_frame["intensity"] > int(Cutoff_Intensity)]


def add_offset():
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
    global date, time
    daytime = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S.%f")
    offset_seconds = offset / 1e6
    daytime += timedelta(seconds=offset_seconds)
    date, time = daytime.strftime("%Y-%m-%d"), daytime.strftime("%H:%M:%S.%f")


def write_time_stamp(date, time):
    """
    Write the date and time to a timestamps file.

    Args:
        date (str): The date in the format "YYYY-MM-DD".
        time (str): The time in the format "HH:MM:SS.mmmmmm".

    Returns:
        None
    """
    timestamps = os.path.join(
        Output_Directory, date, "velodyne_points", "timestamps.txt"
    )
    with open(timestamps, "a") as f:
        f.write(f"{date} {time}\n")


def process_csv_files():
    """
    Removes the extra columns and writes the time stamps.
    """
    csvs_dir = os.path.join(Working_Directory, "VeloView CSVs")
    files = os.listdir(csvs_dir)
    csv_file_names = [file for file in files]
    if not csv_file_names:
        raise Exception("CSV files not found")

    for csv_file_name in csv_file_names:
        csv_file_path = os.path.join(csvs_dir, csv_file_name)
        data_frame = pd.read_csv(csv_file_path)
        if Filter_The_Data:
            data_frame = filter_the_data(data_frame)
        if (
            csv_file_name != csv_file_names[0]
        ):  # Because the first timestamp is read from the pcap file name
            add_offset()
        write_time_stamp(date, time)
        data_frame = data_frame[
            ["Points_m_XYZ:0", "Points_m_XYZ:1", "Points_m_XYZ:2", "intensity"]
        ]
        data_frame.to_csv(csv_file_path, index=False)  # save the csv
    print("Processed CSV files successfully.")


def main():
    print("Application started.")
    init_pipeline()
    process_csv_files()
    print("Application finished successfully.")


if __name__ == "__main__":
    main()
