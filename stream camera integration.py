import velodyne_decoder as vd
import socket
import time
import cv2
import os
from datetime import datetime
from multiprocessing import Process, Queue
import keyboard
from scapy.utils import PcapWriter
from scapy.layers.l2 import Ether
from dotenv import load_dotenv

load_dotenv()
IP = "192.168.1.1"
PORT = 2368
BROADCAST = b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x08\x00"
IPV4 = (
    b"\x45\x00\x04\xd2\x00\x00\x40\x00\xff\x11\xff\xff\xc0\xa8\x00\xc8\xff\xff\xff\xff"
)
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


def stop_stream(processA):
    def stop(key):
        try:
            if key.char == "a":
                processA.terminate()
                DATA_QUEUE.put({"data": "STOP", "time": get_timestamp()})
                PKTS.put({"data": "STOP", "time": get_timestamp()})
                return False  # Stop the listener
        except AttributeError:
            pass  # Non-character keys

    return stop

def record(path):
    # Open the camera
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # Get the default resolutions
    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))

    # Define the codec using VideoWriter_fourcc and create a VideoWriter object
    # We specify output file name "output.mp4", codec "mp4v", FPS as 30.0, and frame size as (frame_width, frame_height)
    out = cv2.VideoWriter(
        "path.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 15.0, (frame_width, frame_height)
    )
    print("Recording...")
    while True:
        ret, frame = cam.read()
        if ret == True:
            # Write the frame to the output file
            out.write(frame)

            # Display the resulting frame (optional)
            # cv2.imshow("Frame", frame)

            # Break the loop on 'q' key press
            if keyboard.is_pressed("esc"):
                print("Recording stopped.")
                break
        else:
            break

    # Release the camera and writer, destroy all windows
    cam.release()
    out.release()
    cv2.destroyAllWindows()


def pcap_encoder():

    start_time = datetime.now()
    os.makedirs(f"{SAVE_FOLDER}/{SUB_DIRECTORY}/{SUB_DIRECTORY}",exist_ok=True)

    processA = Process(target=stream, args=(DATA_QUEUE, PKTS))
    processA.start()
    processC = Process(target=create_pcap, args=(PKTS,))
    processC.start()

    while True:
        if keyboard.is_pressed("a"):
            processA.terminate()
            DATA_QUEUE.put({"data": "STOP", "time": get_timestamp()})
            PKTS.put({"data": "STOP", "time": get_timestamp()})
            break

    # Wait for both processes to finish
    processA.join()
    processC.join()

    end_time = datetime.now()

    print("Recording time : ", end_time - start_time)
