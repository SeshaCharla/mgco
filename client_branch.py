# vim:fileencoding=utf-8
# author: SaiChrla


import socket
import protocol as p
from multiprocessing import Process, Lock
import config


def client_branch(addr, lock):
    """Starts a client to a server and writes the received data in to a
    file"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect(addr)
        frame = bytes()
        trail = bytes()
        frames = []
        while True:
            try:
                data = trail + client_sock.recv(p.BUF_SIZ)
                parts = data.split(p.ETX)
                trail = parts[-1]
                try:
                    frame = parts[-2].lstrip(p.STX)
                    filelockwrite(frame, addr, lock)
                    frames = []    # clear the old frames
                except IndexError:
                    try:
                        frame = frames[-1].lstrip(p.STX)
                        filelockwrite(frame, addr, lock)
                        frames = []    # clear the old frames
                    except IndexError:
                        pass
                finally:
                    try:
                        for bytestr in parts[:-3]:
                            frames.append(bytestr)
                    except IndexError:
                        pass
            except KeyboardInterrupt:
                client_sock.close()
                break
            except:
                time.sleep(10)
                client_branch(addr, lock)       # Restart the client server


def filewrite(frame, addr):
    """writes the fframe in to file named after the sddress"""
    with open("{}_{}.dat".format(addr[0], str(addr[1])), 'w',
            encoding='cp1252') as f:
        f.write(frame.decode('cp1252'))


def filelockwrite(frame, addr, lock):
    """writes to a file to a file named after address with appropriate lock"""
    with open("{}_{}.dat".format(addr[0], str(addr[1])), 'w',
            encoding='cp1252') as f:
        with lock:
            f.write(frame.decode('cp1252'))


def setup_clientbranches(n, addrs, lock_list):
    """sets up the required no. of client branches """
    Clients = [Process(target=client_branch, args=(addrs[i],lock_list[i])) for
            i in range(n)]
    for client in Clients :
        client.start()


if __name__ == "__main__" :

    n, addrs, nparms, st_list = config.get_config()
    lock_list = [Lock() for i in range(n)]
    setup_clientbranches(n, addrs, lock_list)
