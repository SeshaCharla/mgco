# vim:fileencoding=utf-8
# author: SaiChrla

import socket
import time
import protocol as p
from multiprocessing import Lock
import config
import filereader as fl
import client_branch as cb

class PipelineServer:
    """ Creates a pipeline server object"""
    n, addr_list, nparms_list, st_list = config.get_config()   # Configuration
    lock_list = [Lock() for i in range(n)]                # locks for file I/O
    GC_list = [p.GCFrame(nparms) for nparms in nparms_list] # List of GC frames
    ADDR, SLEEP_TIME = config.pipeline_config()   # Addr and sleeptime pipeline

    # Set up the client branches
    cb.setup_clientbranches(n, addr_list, lock_list)

    nparms = sum(nparms_list)

    # The pipeline server
    def __init__(self):
        """ Initiate a pipeline server and listens for connections for ever"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as
        self.PipelineSocket:
            self.PipelineSocket.setsockopt(socket.SOL_SOCKET,
                    socket.SO_REUSEADDR, 1)
            self.PipelineSocket.bind(ADDR)
            while True:
                try:
                    self.PipelineSocket.listen()
                    print("listening for connection at {}:{}",
                            format(ADDR[0],ADDR[1]))
                    tdacs_sock, address = PipelineSocket.accept()
                    print("Connected to {}:{}".format(address[0],address[1]))
                    self.handle_tdacs(tdacs_sock)
                    print("Sending data to {}:{}".format(address[0],address[1]))
                except:
                    break

    def handle_tdacs(self, tdacs_sock):
        """ Handles the tdacs client """
        while True:
            try:
                frame_list = [fl.filelockread(self.addr_list[i], self.lock_list[i])
                        for i in range(self.n)]
                for i in range(self.n):
                    self.GC_list[i].update_frame(frame_list[i])
                frametype = p.setframetype(self.GC_list)
                headerbytes = p.creatheader(self.nparms, frametype)
                data_list = [gc.data for gc in self.GC_list]
                data = bytes()
                for line in data_list:
                    data = data+line
                frame = p.STX + headerbytes + data + p.ETX
                tdacs_sock.sendall(frame)
                time.sleep(self.SLEEP_TIME)
            except:
                tdacs_sock.close()
                break


if __name__ == "__main__":
    PipelineServer()

