# vim:fileencoding=utf-8
# author: SaiChrla


import socket
import protocol as p
import time
import config

ADDR, s = config.pipeline_config()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tdacs:
    tdacs.connect(ADDR)
    frame = bytes()
    trail = bytes()
    while True:
        data = trail + tdacs.recv(p.BUF_SIZ)
        parts = data.split(p.ETX)
        trail = parts[-1]
        try:
            frame = parts[-2].lstrip(p.STX)
            print(frame.decode('cp1252'))
        except IndexError:
            pass
        except KeyboardInterrupt:
            tdacs.close()
            break
        except ConnectionError:
            tdacs.close()

