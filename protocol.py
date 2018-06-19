# vim:fileencoding=utf-8
# AUthor: SaiChrla


""" This file has the necessary functions for readign and wrinting data in GCO
protocol. cp1252 encoding is used as '\xbb' and '\xcc' are represented by
corresponding hex nos. unlike utf-8 where is split in to 2 nos. """

import datetime as dt

# Frame Headers
STX = bytes('\x02', 'cp1252')
ETX = bytes('\x03', 'cp1252')
DATA_FRAME = bytes('\xbb', 'cp1252')
DB_FRAME = bytes('\xcc', 'cp1252')
INVALID = bytes('\x00', 'cp1252')


#Test local address
TEST_HOST = '127.0.0.1'
TEST_PORT = 4040
TEST_ADDR = (TEST_HOST, TEST_PORT)

# Buffer Size
BUF_SIZ = 4096  # 4 MB


class GCFrame:
    """frame objects for storing current data"""
    DATA = True
    DB = False

    __init__(self, noparms):
        """Initial the gco-data object"""
        self.noparms = noparms
        self.timestr = bytes(17, encoding='cp1252')
        self.paramsstr = bytes(4, encoding=)
        self.data = bytes(noparams, encoding='cp1252'))
        self.invalid_data = no_of_params * bytes('+0000999', encoding='cp1252')
        self.old_timestamp = dt.datetime.now()
        self.type = DATA

    def update_frame(self, frame):
        """ update the gc-frame attributes """
        if self.invalid(frame):
            self.set_invalid()
        else:
            self.header = self.get_header(frame)     #frame[1:22]
            self.data = self.get_data(frame)    #frame[27:]
            self.set_type(frame)
            self.old_timestamp = self.get_timestamp(frame)

    def invalid(self, frame):
        """ Returns the truth value of invalidity"""
        if (self.get_timestamp(frame) <= self.old_timestamp and
            self.get_noparms() != self.noparams):
            return True
        else:
            return False

    def set_invalid(self):
        """Makes the frame invalid"""
        self.data = self.invalid_data

    def get_noparms(self, frame):
        """Get the no. of parameters"""
        try:
            return len(self.get_data(frame))/8
        except:
            return 0

    def check_parms(self, frame):
        """ Check if the params are same"""
        try:
            return len(self.get_data(frame))/8 == int(self.get_header()[-4:])
        except:
            return False

    def get_data(self, frame):
        """ Get the data part of the frame"""
        try:
            return frame[27:]
        except:
            self.invalid_data

    def get_header(self, frame):
        """ Get the header from the data"""
        try:
            return frame[1:27]
        except:
            return bytes(27)








