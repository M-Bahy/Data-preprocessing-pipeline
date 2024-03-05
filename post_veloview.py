import os
from dotenv import load_dotenv

load_dotenv()
Working_Directory = os.getenv("WORKING_DIRECTORY")
pcap_file_name = ""
csv_file_names = []


def scan_directory():
    global pcap_file_name, csv_file_names
    files = os.listdir(Working_Directory)
    csv_file_names = [file for file in files if file.endswith(".csv")]
    if not csv_file_names:
        raise Exception("CSV file not found")
    pcap_files = [file for file in files if file.endswith(".pcap")]
    if not pcap_files:
        raise Exception("PCAP file not found")
    pcap_file_name = pcap_files[0]


scan_directory()
print(pcap_file_name)
