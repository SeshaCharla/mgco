# vim:fileencoding=utf-8
# author: SaiChrla


import socket
import protocol as p
import time
import config


def gcserver(addr, nparms, st):
    """Starts a gc server with the given address"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as GCOServerSocket:
        GCOServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        GCOServerSocket.bind(addr)
        while True:
            GCOServerSocket.listen()
            client_sock, adds = GCOServerSocket.accept()
            while True:
                try:
                    client_sock.sendall(p.get_frame(nparms))
                    time.sleep(st)
                except KeyboardInterrupt:
                    client_sock.close()
                    break


if __name__ == "__main__" :
    from multiprocessing import Process
    import config

    n, addr_list, nparms_list, st_list = config.get_config()
    GCServers = [Process(target=gcserver, args=(addr_list[i], nparms_list[i],
        st_list[i])) for i in range(n)]
    for server in GCServers:
        server.start()
