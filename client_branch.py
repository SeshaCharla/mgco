# vim:fileencoding=utf-8
# author: SaiChrla


import socket
import protocol as p

def client_branch(host, port, write_type='w'):
    """Starts a client to a server and writes the received data in to a
    file"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect((host, port))
        frame = bytes()
        trail = bytes()
        frames = []
        while True:
            data = trail + client_sock.recv(p.BUF_SIZ)
            parts = data.split(p.ETX)
            trail = parts[-1]
            try:
                frame = parts[-2][1:]
                # print(frame.decode('cp1252'))
                with open("{}_{}.dat".format(host, str(port)), write_type,
                        encoding='cp1252') as f:
                    f.write(frame.decode('cp1252'))
            except IndexError:
                try:
                    frame = frames[-1]
                    with open("{}_{}.dat".format(host, str(port)), write_type,
                            encoding='cp1252') as f:
                        f.write(frame.decode('cp1252'))
                except IndexError:
                    pass
            finally:
                try:
                    for bytestr in parts[:-3]:
                        frames.append(bytestr)
                except IndexError:
                    pass


if __name__ == "__main__":
    client_branch(p.TEST_HOST, p.TEST_PORT)

