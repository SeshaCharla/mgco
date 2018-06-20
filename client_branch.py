# vim:fileencoding=utf-8
# author: SaiChrla


import socket
import protocol as p

def client_branch(host, port):
    """Starts a client to a server and writes the received data in to a
    file"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect((host, port))
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
                    # print(frame.decode('cp1252'))
                    filewrite(frame, host, port)
                    frames = []    # clear the old frames
                except IndexError:
                    try:
                        frame = frames[-1].lstrip(p.STX)
                        filewrite(frame, host, port)
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


def filewrite(frame, host, port):
    """writes the fframe in to file named after the sddress"""
    with open("{}_{}.dat".format(host, str(port)), 'w',
            encoding='cp1252') as f:
        f.write(frame.decode('cp1252'))


if __name__ == "__main__":
    client_branch(p.TEST_HOST, p.TEST_PORT)

