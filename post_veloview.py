import os
import shutil
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
Working_Directory = os.getenv("Working_Directory")
Output_Directory = os.getenv("Output_Directory")
Cutoff_Intensity = os.getenv("Cutoff_Intensity")
Filter_The_Data = os.getenv("Filter_The_Data") == "True"
pcap_file_name = ""
csv_file_names = []
date = ""


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


def csv_folder_hierarchy():
    """
    Organizes CSV files into separate directories based on whether they are original or filtered.

    This function moves all CSV files in the working directory to a subdirectory named "VeloView Original CSVs".
    If the `Filter_The_Data` flag is set to True, it also copies the CSV files to another subdirectory named
    "VeloView Filtered CSVs".

    The directories are created if they do not already exist.
    """
    original_csvs_dir = os.path.join(Working_Directory, "VeloView Original CSVs")
    os.makedirs(original_csvs_dir, exist_ok=True)
    original_csvs_dir = os.path.join(Working_Directory, "CloudCompare Output")
    os.makedirs(original_csvs_dir, exist_ok=True)
    # if Filter_The_Data:
    #     filtered_csvs_dir = os.path.join(Working_Directory, "VeloView Filtered CSVs")
    #     os.makedirs(filtered_csvs_dir, exist_ok=True)
    for csv_file_name in csv_file_names:
        original_path = os.path.join(Working_Directory, csv_file_name)
        shutil.move(original_path, original_csvs_dir)
        # if Filter_The_Data:
        #     new_path = os.path.join(original_csvs_dir, csv_file_name)
        #     shutil.copy(new_path, filtered_csvs_dir)


def decode_pcap_file_name():
    """
    Extracts the data from the PCAP file name.
    """
    global date
    datetime = pcap_file_name.split("_")[0]
    date = f"{datetime[:4]}-{datetime[5:7]}-{datetime[8:10]}"


def output_folder_hierarchy():
    """
    Creates a folder hierarchy for storing output files.
    """
    global date
    output_dir = os.path.join(Output_Directory, date)
    os.makedirs(output_dir, exist_ok=True)
    velodyne_dir = os.path.join(output_dir, "velodyne_points")
    os.makedirs(velodyne_dir, exist_ok=True)
    timestamps_start_path = os.path.join(velodyne_dir, "timestamps_start.txt")
    with open(timestamps_start_path, "w") as f:
        pass
    timestamps_end_path = os.path.join(velodyne_dir, "timestamps_end.txt")
    with open(timestamps_end_path, "w") as f:
        pass
    timestamps = os.path.join(velodyne_dir, "timestamps.txt")
    with open(timestamps, "w") as f:
        pass
    data_dir = os.path.join(velodyne_dir, "data")
    os.makedirs(data_dir, exist_ok=True)


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


def write_timestamps(start, end, avg):
    pass


def process_csv_files():
    """
    Removes the extra columns and writes the time stamps.
    """
    original_csvs_dir = os.path.join(Working_Directory, "VeloView Original CSVs")
    files = os.listdir(original_csvs_dir)
    csv_file_names = [file for file in files]
    if not csv_file_names:
        raise Exception("CSV files not found")
    for csv_file_name in csv_file_names:
        csv_file_path = os.path.join(original_csvs_dir, csv_file_name)
        data_frame = pd.read_csv(csv_file_path)
        start_timestamp = data_frame["adjustedtime"][0]
        end_timestamp = data_frame["adjustedtime"].iloc[-1]
        avg_timestamp = (start_timestamp + end_timestamp) / 2
        write_timestamps(start_timestamp, end_timestamp, avg_timestamp)
        data_frame = data_frame[
            ["Points_m_XYZ:0", "Points_m_XYZ:1", "Points_m_XYZ:2", "intensity"]
        ]
        data_frame.to_csv(csv_file_path, index=False)  # save the csv


def main():
    # print("Application started , please wait this may take a while.")
    # init_pipeline()
    # process_csv_files()
    # print("Application finished successfully.")
    process_csv_files()
    pass


if __name__ == "__main__":
    main()
