# vim:fileencoding=utf-8
# author: SaiChrla


import socket
import protocol as p
from multiprocessing import Process, Lock
import config
from filelockio import filelockwrite
import time


def client_branch(addr, lock, st):
    """Starts a client to a server and writes the received data in to a
    file"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.settimeout(3*st)
        frame = bytes()
        trail = bytes()
        frames = []
        client_sock.connect(addr)
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
            except:
                client_sock.close()
                raise


def inf_client_branch(addr, lock, st):
    """Runs the client branch function and handles other exceptions"""
    while True:
        try:
            client_branch(addr, lock, st)
        except OSError or ConnectionError:
            print("TimeOutError: GCO Server not responding")
            time.sleep(st)
            print("Restarting the client to {}".format(addr[0]))
            continue
        except KeyboardInterrupt:
            break


def setup_clientbranches(n, addrs, lock_list, st_list):
    """sets up the required no. of client branches """
    Clients = [Process(target=inf_client_branch, args=(addrs[i],lock_list[i],
        st_list[i])) for i in range(n)]
    for client in Clients :
        client.start()


if __name__ == "__main__" :

    n, addrs, nparms, st_list = config.get_config()
    lock_list = [Lock() for i in range(n)]
    setup_clientbranches(n, addrs, lock_list, st_list)
