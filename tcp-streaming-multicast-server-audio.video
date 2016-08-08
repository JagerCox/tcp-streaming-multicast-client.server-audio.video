#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import socket
import base64
import pyaudio
import numpy as np
from threading import Thread

"""
    File name: tcp-streaming-multicast-server-audio.video.py
    Author: Jäger Cox // jagercox@gmail.com
    Date created: 08/08/2016
    License: MIT
    Python Version: 2.7
    Code guide line: PEP8
"""

__author__ = "Jäger Cox // jagercox@gmail.com"
__created__ = "08/08/2016"
__license__ = "MIT"
__version__ = "0.1"
__python_version__ = "2.7"
__email__ = "jagercox@gmail.com"

# Sockets channels
IP_SERVER = "0.0.0.0"
VIDEO_SERVER_PORT = 11111
AUDIO_SERVER_PORT = 11112
MAX_NUM_CONNECTIONS = 20

# Webcam configuration
VIDEOCAM_INDEX = 0

# PyAudio configuration
SIZE_PACKAGE = 1024
CHUNK = 1024
CHANNELS = 1
RATE = 10240
INPUT = True
FORMAT = pyaudio.paInt16


class connection_pool_audio(Thread):
    def __init__(self, ip, port, conn, device):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.device = device
        print "[+][.audio] New server socket thread started for " + ip + \
            ":" + str(port)

    def run(self):
        while True:
            data = self.device.read(CHUNK)
            self.conn.send(data)
            self.conn.recv(SIZE)
        self.conn.close()

class connection_pool_video(Thread):
    def __init__(self, ip, port, conn, device):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.device = device
        print "[+][.video] New server socket thread started for " + self.ip + \
            ":" + str(self.port)

    def run(self):
        try:
            while True:
                ret, frame = self.device.read()
                data = frame.tostring()
                self.conn.sendall(base64.b64encode(data) + '\r\n')
        except:
            print "Connection lost with " + self.ip + ":" + str(self.port)
        self.conn.close()


def tcp_audio_thread():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=INPUT,
                    frames_per_buffer=CHUNK)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((IP_SERVER, AUDIO_SERVER_PORT))
    connection.listen(MAX_NUM_CONNECTIONS_LISTENER)
    while True:
        (conn, (ip, port)) = connection.accept()
        t = connection_pool_audio(ip, port, conn, stream)
        t.start()
    stream.stop_stream()
    stream.close()
    p.terminate()


def tcp_video_thread():
    camera = cv2.VideoCapture(VIDEOCAM_INDEX)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((IP_SERVER, VIDEO_SERVER_PORT))
    connection.listen(MAX_NUM_CONNECTIONS_LISTENER)
    while True:
        (conn, (ip, port)) = connection.accept()
        t = connection_pool_video(ip, port, conn, camera)
        t.start()
    camera.release()


if __name__ == '__main__':
    print "Starting..."
    thread_audio = Thread(target=tcp_audio_thread)
    thread_video = Thread(target=tcp_video_thread)
    thread_audio.start()
    thread_video.start()
