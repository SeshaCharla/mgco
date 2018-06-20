# vim:fileencoding=utf-8
# author: SaiChrla


import socket
import gctestframes as tg
import protocol
import time


def gcserver(addr):
    """Starts a gc server with the given address"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as GCOServerSocket:
        GCOServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        GCOServerSocket.bind(addr)
        GCOServerSocket.listen()
        client_sock, adds = GCOServerSocket.accept()
        while True:
            try:
                for frame in tg.get_frames():
                    client_sock.sendall(frame)
                    time.sleep(1)
            except KeyboardInterrupt:
                client_sock.close()
                break

if __name__ == "__main__" :
    from multiprocessing import Process
    import config

    n, addrs, nparms = config.get_config()
    GCServers = [Process(target=gcserver, args=(addrs[i],)) for i in range(n)]
    for server in GCServers:
        server.start()
