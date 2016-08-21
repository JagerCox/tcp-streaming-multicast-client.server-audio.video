#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import socket
import base64
import pyaudio
import numpy as np
from threading import Thread

"""
    File name: tcp-streaming-multicast-client-audio.video.py
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

# Sockets channels configuration
IP_SERVER = "0.0.0.0"
VIDEO_SERVER_PORT = 11111
AUDIO_SERVER_PORT = 11112
TIMEOUT_SOCKET = 10

# Webcam configuration
IMAGE_HEIGHT = 480
IMAGE_WIDTH = 640
COLOR_PIXEL = 3  # RGB

# PyAudio configuration
SIZE = 1024
CHANNELS = 1
RATE = 10240
INPUT = True
FORMAT = pyaudio.paInt16


def audio_thread(socket_connection):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    INPUT=INPUT)

    while True:
        data = socket_connection.recv(SIZE)
        if data:
            stream.write(data)

    socket_connection.close()
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    # Socket video initialization
    connection_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_video.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection_video.settimeout(TIMEOUT_SOCKET)

    # Socket audio initialization
    connection_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_audio.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection_audio.settimeout(TIMEOUT_SOCKET)

    # Connect channels
    connection_video.connect((IP_SERVER, VIDEO_SERVER_PORT))
    connection_audio.connect((IP_SERVER, AUDIO_SERVER_PORT))

    # Create a thread for audio channel
    t_audio = Thread(target=audio_thread, args=(connection_audio,))
    t_audio.start()

    # Main thread video
    while True:
        try:
            # Recept video data
            fileDescriptor = connection_video.makefile(mode='rb')
            result = fileDescriptor.readline()
            fileDescriptor.close()

            # Create image
            result = base64.b64decode(result)
            frame = np.fromstring(result, dtype=np.uint8)
            frame_matrix = np.array(frame)
            frame_matrix = np.reshape(frame_matrix, (IMAGE_HEIGHT, IMAGE_WIDTH,
                                                     COLOR_PIXEL))

            # Show viewer
            cv2.imshow('Client', frame_matrix)

            # Terminate
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print "[Error] " + str(e)

    cv2.destroyAllWindows()
    connection_video.close()
