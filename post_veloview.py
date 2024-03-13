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
pcap_file_name = ""
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


def init_pipeline():
    """
    Initializes the data preprocessing pipeline.
    """
    scan_directory()
    decode_pcap_file_name()
    output_folder_hierarchy()


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
    Process CSV files in the Working_Directory and convert them to TXT files.

    This function reads each CSV file in the Working_Directory, applies optional data filtering,
    converts the columns to a specific format (x y z intensity), and saves the resulting data as TXT files,
    In the output directory. The function also writes the timestamps of the TXT files to a timestamps file.
    Each timestamp is written in the format "YYYY-MM-DD HH:MM:SS.mmmmmm" and represents the time of the
    corresponding TXT file.

    Raises:
        Exception: If no CSV files are found in the Working_Directory.

    Returns:
        None
    """
    files = os.listdir(Working_Directory)
    csv_file_names = [file for file in files if file.endswith(".csv")]
    csv_file_names.sort(key=lambda file: int(file.split(" ")[-1].split(".")[0][:-1]))
    if not csv_file_names:
        raise Exception("CSV files not found")
    count = 0
    for csv_file_name in csv_file_names:
        csv_file_path = os.path.join(Working_Directory, csv_file_name)
        data_frame = pd.read_csv(csv_file_path)
        if csv_file_name != csv_file_names[0]:
            add_offset()
        write_time_stamp(date, time)
        data_frame = data_frame[
            ["Points_m_XYZ:0", "Points_m_XYZ:1", "Points_m_XYZ:2", "intensity"]
        ]
        data_frame = data_frame.applymap(lambda x: f"{float(x):.8f}")
        count_str = str(count).zfill(6)
        txt_path = os.path.join(
            Output_Directory, date, "velodyne_points", "data", f"{count_str}.txt"
        )
        data_frame.to_csv(txt_path, sep=" ", header=False, index=False)
        count += 1
        if count % 10 == 0:
            print(f"Processed {count} CSV files.")
    print("Processed CSV files successfully.")


def main():
    print("Application started.")
    init_pipeline()
    process_csv_files()
    print("Application finished successfully.")


if __name__ == "__main__":
    main()
