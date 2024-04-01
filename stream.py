import velodyne_decoder as vd
import socket
import sys
import time
import csv
import os
import numpy as np
from datetime import datetime
from multiprocessing import Process, Queue
from pynput import keyboard
from scapy.all import wrpcap, Raw
from scapy.utils import PcapWriter
from scapy.layers.l2 import Ether
from dotenv import load_dotenv, set_key

load_dotenv()
IP = "192.168.1.1"
PORT = 2368
BROADCAST = b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x08\x00"
IPV4 = b"\x45\x00\x04\xd2\x00\x00\x40\x00\xff\x11\xff\xff\xc0\xa8\x00\xc8\xff\xff\xff\xff"
UDP = b"\x09\x40\x09\x40\x04\xbe\x00\x00"
HEADERS = BROADCAST + IPV4 + UDP
DATA_QUEUE = Queue(-1)
PKTS = Queue(-1)
SAVE_FOLDER = os.getenv("SAVE_FOLDER")
SUB_DIRECTORY = os.getenv("SUB_DIRECTORY")


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S.%f")


def get_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_time():
    return datetime.now().strftime("%H:%M:%S.%f")


def read_live_data(ip, port, PKTS, as_pcl_structs=False):
    decoder = vd.StreamDecoder()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))
    while True:
        data, address = s.recvfrom(vd.PACKET_SIZE * 2)
        recv_stamp = time.time()
        PKTS.put({"data": data, "time": recv_stamp})
        yield decoder.decode(recv_stamp, data, as_pcl_structs)


def stream(DATA_QUEUE, PKTS):
    for Data in read_live_data(IP, PORT, PKTS):
        if Data != None:
            stamp, points = Data
            stamp = str(get_timestamp())
            print(len(points))
            DATA_QUEUE.put({"data": points, "time": stamp})


def convert_to_csv(DATA_QUEUE):
    processed = 0
    while True:
        if not DATA_QUEUE.empty():
            # print("Queue size : ", DATA_QUEUE.qsize())
            dequeued = DATA_QUEUE.get()
            if not isinstance(dequeued["data"], np.ndarray):
                # print("processB received stop signal from processA. Stopping processB.")
                print("Total number of packets converted to csv : ", processed)
                break
            points = dequeued["data"]
            timestamp = dequeued["time"]
            # print("The save folder is : ", SAVE_FOLDER)
            # print("The sub directory is : ", SUB_DIRECTORY)
            processed += 1
            with open(
                f"{SAVE_FOLDER}/{SUB_DIRECTORY}/{timestamp}.csv", "w", newline=""
            ) as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "Points_m_XYZ:0",
                        "Points_m_XYZ:1",
                        "Points_m_XYZ:2",
                        "intensity",
                    ]
                )
                for point in points:
                    y = point[0]
                    x = -point[
                        1
                    ]  # because the decoder is following the ROS coordinate system
                    z = point[2]
                    intensity = point[3]
                    writer.writerow([x, y, z, intensity])


def on_press(key):
    try:
        if key.char == "a":
            processA.terminate()
            # print("Stopped processA due to 'a' key press.")
            DATA_QUEUE.put({"data": "STOP", "time": get_timestamp()})
            PKTS.put({"data": "STOP", "time": get_timestamp()})
            return False  # Stop the listener
    except AttributeError:
        pass  # Non-character keys


def create_pcap(PKTS):
    pcap_writer = PcapWriter(
        f"{SAVE_FOLDER}/{SUB_DIRECTORY}/{SUB_DIRECTORY}.pcap", linktype=1
    )
    counter = 0
    while True:
        pkt = PKTS.get()
        if pkt["data"] == "STOP":
            # print("processC received stop signal from processA. Stopping processC.")
            print("Total number of packets written to pcap file : ", counter)
            break
        counter += 1
        kimo = Ether(HEADERS + pkt["data"])
        kimo.time = pkt["time"]
        pcap_writer.write(kimo)


if __name__ == "__main__":
    # Set the values in the .env file
    start_time = datetime.now()
    set_key(".env", "SUB_DIRECTORY", str(get_timestamp()))
    set_key(".env", "SAVE_FOLDER", "SAVE_FOLDER")
    if not os.path.exists(f"{SAVE_FOLDER}/{SUB_DIRECTORY}"):
        os.makedirs(f"{SAVE_FOLDER}/{SUB_DIRECTORY}")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    processA = Process(target=stream, args=(DATA_QUEUE, PKTS))
    processA.start()
    processB = Process(target=convert_to_csv, args=(DATA_QUEUE,))
    # processB.start()
    processC = Process(target=create_pcap, args=(PKTS,))
    processC.start()
    
    # Wait for both processes to finish
    processA.join()
    # processB.join()
    processC.join()
    
    end_time = datetime.now()
    
    print("execution time : " , end_time - start_time)
