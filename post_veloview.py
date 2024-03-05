import os




files = os.listdir(".")
csv_files = [file for file in files if file.endswith(".csv")]
if not csv_files:
    raise Exception("CSV file not found")
pcap_files = [file for file in files if file.endswith(".pcap")]
if not pcap_files:
    raise Exception("PCAP file not found")
print(pcap_files)
