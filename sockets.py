# vim:fileencoding=utf-8
# Author: SaiChrla

""" this file has the code for creating sockets for servers and clients"""


import socket
import protocol as p

class Client:
    """ General class for clinet sockets with given protocol"""

    def __init__(self, server_addr):
        self.socket = socket.socket(socket.AF_INET, socket.SOC_STREAM)
        self.sockket.connect(server_addr)
        self.trail = bytes()
        self.frame = bytes()

    def recv_frame(self):
        """ receive a full frame of data """
        recvd_frame = False
        while not recvd_frame:
            recvd = self.socket.recv(p.BUF_SIZ)
            stream = self.trail + recvd
            parts = stream.split(p.ETX)
            self.trail = parts[-1]
            try:
                self.frame = parts[-2][1:]
                recvd_frame = True
            except IndexError:
                recvd_frame = False

    def recv_data(self):
        """ start receiving data """
        while True:
            try:
                self.recv_frame()
                with \
                open('{}_data.txt'.format(str(self.socket.getsockname()[1])),
                        'a') as f:
                    f.write(decode(self.frame, 'cp1252'))
            except KeyboardInterrupt:
                self.socket.close()


