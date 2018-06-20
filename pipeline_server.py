# vim:fileencoding=utf-8
# author: SaiChrla

import socket
import time
import protocol as p
from multiprocessing import Lock
import config
import filereader as fl
import client_branch as cb
from pprint import pprint


n, addr_list, nparms_list = config.get_config()      # Configuration
lock_list = [Lock() for i in range(n)]     # locks for file I/O
GC_list = [p.GCFrame(nparms) for nparms in nparms_list]   # List of GC frames
ADDR, SLEEP_TIME = config.pipeline_config()    # Address and sleeptime pipeline

cb.setup_clientbranches(n, addr_list, lock_list)


# The pipeline server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as PipelineSocket:
    PipelineSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    PipelineSocket.bind(ADDR)
    PipelineSocket.listen()
    tdacs_sock, address = PipelineSocket.accept()
    while True:
        frame_list = [fl.filelockread(addr_list[i], lock_list[i]) for i in
                range(n)]
        for i in range(n):
            GC_list[i].update_frame(frame_list[i])
        frametype = p.setframetype(GC_list)
        nparms = sum(nparms_list)
        headerbytes = p.creatheader(nparms, frametype)
        data_list = [gc.data for gc in GC_list]
        data = bytes().join(data_list)
        frame = p.STX + headerbytes + data + p.ETX
        tdacs_sock.sendall(frame)
        time.sleep(SLEEP_TIME)

