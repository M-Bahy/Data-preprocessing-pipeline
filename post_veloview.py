import os
import shutil
from dotenv import load_dotenv

load_dotenv()
Working_Directory = os.getenv("Working_Directory")
Cutoff_Intensity = os.getenv("Cutoff_Intensity")
Filter_The_Data = os.getenv("Filter_The_Data") == "True"
pcap_file_name = ""
csv_file_names = []


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
        raise Exception("CSV file not found")
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
    if Filter_The_Data:
        filtered_csvs_dir = os.path.join(Working_Directory, "VeloView Filtered CSVs")
        os.makedirs(filtered_csvs_dir, exist_ok=True)
    for csv_file_name in csv_file_names:
        original_path = os.path.join(Working_Directory, csv_file_name)
        shutil.move(original_path, original_csvs_dir)
        if Filter_The_Data:
            new_path = os.path.join(original_csvs_dir, csv_file_name)
            shutil.copy(new_path, filtered_csvs_dir)


def create_folder_hierarchy():
    csv_folder_hierarchy()


scan_directory()
