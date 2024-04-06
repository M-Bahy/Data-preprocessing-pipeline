import velodyne_decoder as vd
import socket
import sys
import time
import csv
import os
import numpy as np
from datetime import datetime
from multiprocessing import Process, Queue
import keyboard
from scapy.all import wrpcap, Raw
from scapy.utils import PcapWriter
from scapy.layers.l2 import Ether
from dotenv import load_dotenv, set_key

load_dotenv()
IP = "192.168.1.1"
PORT = 2368
BROADCAST = b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x08\x00"
IPV4 = (
    b"\x45\x00\x04\xd2\x00\x00\x40\x00\xff\x11\xff\xff\xc0\xa8\x00\xc8\xff\xff\xff\xff"
)
UDP = b"\x09\x40\x09\x40\x04\xbe\x00\x00"
HEADERS = BROADCAST + IPV4 + UDP
CAMERA_SIGNAL = Queue(-1)
PKTS = Queue(-1)
SAVE_FOLDER = os.getenv("SAVE_FOLDER")
SUB_DIRECTORY = os.getenv("SUB_DIRECTORY")


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S.%f")


def get_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_time():
    return datetime.now().strftime("%H:%M:%S.%f")


def read_live_data(ip, port, PKTS, CAMERA_SIGNAL,as_pcl_structs=False):
    decoder = vd.StreamDecoder()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))
    counter = 1
    while True:
        data, address = s.recvfrom(vd.PACKET_SIZE * 2)
        recv_stamp = time.time()
        PKTS.put({"data": data, "time": recv_stamp})
        if counter == 1:
            CAMERA_SIGNAL.put("START")
            counter = -1
        yield decoder.decode(recv_stamp, data, as_pcl_structs)


def stream( PKTS,CAMERA_SIGNAL):
    for Data in read_live_data(IP, PORT, PKTS,CAMERA_SIGNAL):
        if Data != None:
            stamp, points = Data
            print(len(points))


def create_pcap(PKTS):
    pcap_writer = PcapWriter(
        f"{SAVE_FOLDER}/{SUB_DIRECTORY}/{SUB_DIRECTORY}.pcap", linktype=1
    )
    counter = 0
    while True:
        pkt = PKTS.get()
        if pkt["data"] == "STOP":
            print("Total number of packets written to pcap file : ", counter)
            break
        counter += 1
        kimo = Ether(HEADERS + pkt["data"])
        kimo.time = pkt["time"]
        pcap_writer.write(kimo)
        # if counter == 1:
        #     with open(f"{SAVE_FOLDER}/{SUB_DIRECTORY}/time.txt", "w") as file:
        #         file.write(str(pkt["time"]))

def fake_camera(CAMERA_SIGNAL):
    start = CAMERA_SIGNAL.get()
    if start == "START":
        print("Camera started")
    stop = CAMERA_SIGNAL.get()
    if stop == "STOP":
        print("Camera stopped")

def pcap_encoder():

    start_time = datetime.now()
    os.makedirs(f"{SAVE_FOLDER}/{SUB_DIRECTORY}/{SUB_DIRECTORY}",exist_ok=True)

    processA = Process(target=stream, args=( PKTS,CAMERA_SIGNAL))
    processA.start()
    processB = Process(target=fake_camera, args=(CAMERA_SIGNAL,))
    processB.start()
    processC = Process(target=create_pcap, args=(PKTS,))
    processC.start()

    while True:
        if keyboard.is_pressed("esc"):
            processA.terminate()
            PKTS.put({"data": "STOP", "time": get_timestamp()})
            CAMERA_SIGNAL.put("STOP")
            print("Recording stopped")
            break

    # Wait for both processes to finish
    processA.join()
    processC.join()

    end_time = datetime.now()

    print("Recording time : ", end_time - start_time)


if __name__ == "__main__":
    pcap_encoder()