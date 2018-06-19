# vim:fileencoding=utf-8
# author: SaiChrla


import socket
import gctestframes as tg
import protocol
import time


HOST = protocol.TEST_HOST
PORT = protocol.TEST_PORT
ADDR = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as GCOServerSocket:
    GCOServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    GCOServerSocket.bind(ADDR)
    GCOServerSocket.listen()
    client_sock, addr = GCOServerSocket.accept()
    for frame in tg.get_frames():
        client_sock.sendall(frame)
        time.sleep(1)
    client_sock.close()

