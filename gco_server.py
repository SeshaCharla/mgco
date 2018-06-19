# vim:fileencoding=utf-8
# author: SaiChrla


import socketserver
from ... import primitives.handlers as h
from ... import primitives.protocol as p
import threading

GcoServer = socketserver.ThreadingTCPServer(p.TEST_ADDR, h.SendTestData)
with GcoServer:
    ip, port = GcoServer.server_address
    # start the server in a thread which creats thread for eac client processes
    GcoServer_thread = threading.Thread(target=GcoServer.serve_forever)
    GcoServer_thread.daemon = True
    server_thread.start()

