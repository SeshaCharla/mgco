# vim:fileencoding=utf-8
# author: SaiChrla


import serversocket
from test.gctestframes import get_frames
import time


class SendTestData(serversocket.BaseRequestHandler):
    """ Sends the test stream of data for program testing."""

    def setup(self):
        # creat the stream
        self.bytestream = get_frames()

    def handle(self):
        # send the stream one by one
        for stream in bytestream:
            self.request.sendall(stream)
            time.sleep(8)
        print("sent data to {} through {} from {}".format(self.request,
            self.client_address, self.server))

    def finish(self):
        # clear the stream
        del self.bytestream

