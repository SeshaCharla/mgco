# vim:fileencoding=utf-8
# author: SaiChrla

import socket
import time
import protocol as p
import multiprocessing import Lock
import config
import filereader as fl
import client_branch as cb

n, addrs, nprms = config.get_config()      # Configuration
lock_list = [Lock() for i in range(n)]     # locks for file I/O
GCOs = [p.GCFrame(noparms) for noparms in nprms]   # List of GC frames
ADDR, SLEEP_TIME = config.pipeline_config()    # Address and sleeptime pipeline

cb.setup_clientbranches(n, addrs, lock_list)


# The pipeline server
with socket.socket(socket.AF_INET, socker.SOCK_STREAM) as PipelineSocket:
    PipelineSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    PipelineSocket.bind(ADDR)
    PipelineSocket.listen()
    tdacs_sock, address = PipelineSocket.accept()
    while True:

