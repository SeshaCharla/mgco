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

DATA = True
DB = False

# Buffer Size
BUF_SIZ = 4096  # 4 MB


def creatheader(nparms, frametype):
    """ Creates the header for the data"""
    t = dt.datetime.now()
    b = lambda x,n=2: bytes(str(x), encoding='cp1252').rjust(n, '0'.encode('cp1252'))
    year = b(t.year, n=4)
    month = b(t.month)
    day = b(t.day)
    hr = b(t.hour)
    mins = b(t.minute)
    sec = b(t.second)
    # ddmmyyyyhhmmss000
    timebytes = day+month+year+hr+mins+sec+'000'.encode('cp1252')
    if frametype:
        frametypebyte = DATA_FRAME
    else:
        frametypebyte = DB_FRAME
    nparmsbytes = b(nparms, n=4)
    return frametypebyte + timebytes + nparmsbytes + (' '*5).encode('cp1252')


def setframetype(GC_list):
    """ Sets the frame type for the concatenated frame"""
    ftypes = [gc.type for gc in GC_list]
    if any(ftypes):
        for gc in GC_list:
            if not gc.type:
                gc.set_invalid()
        return DATA
    else:
        return DB


class GCFrame:
    """frame objects for storing current data"""
    # Frame details (Afterf stripping STX and ETX):
    # frame[0] = frame type (DATA, DB)
    # frame[1:18] = time stamp
    # frame[18:22] = no. of parms
    # frame[22:27] = white spaces
    # frame[27:] = data


    def __init__(self, nparms):
        """Initial the gco-data object"""
        self.nparms = nparms
        self.invalid_data = self.nparms * bytes('+0000999', encoding='cp1252')
        self.old_timestamp = dt.datetime(2018, 4, 22)
        self.type = DATA
        self.data = bytes(''*nparms, encoding='cp1252')

    def update_frame(self, frame):
        """ update the gc-frame attributes """
        if self.invalid(frame):
            self.set_invalid()
        else:
            self.data = self.get_data(frame)    #frame[27:]
            self.set_type(frame)
            self.old_timestamp = self.get_timestamp(frame)

    def invalid(self, frame):
        """ Returns the truth value of invalidity"""
        if (self.get_timestamp(frame) <= self.old_timestamp and
            self.get_nparms(frame) != self.nparms):
            return True
        else:
            return False

    def set_invalid(self):
        """Makes the frame invalid"""
        self.data = self.invalid_data
        self.type = DATA

    def get_nparms(self, frame):
        """Get the no. of parameters"""
        try:
            return len(self.get_data(frame))/8
        except:
            return 0

    def check_nparms(self, frame):
        """ Check if the parms are same"""
        try:
            return len(self.get_data(frame))/8 == int(frame[18:22])
        except:
            return False

    def get_data(self, frame):
        """ Get the data part of the frame"""
        try:
            return frame[27:]
        except:
            return self.invalid_data

    def set_type(self, frame):
        """ set the type of frame"""
        try:
            d = frame[0]
            if d == DATA_FRAME :
                self.type = DATA
            elif d == DB_FRAME :
                self.type = DB
            else:
                self.type = DATA
        except:
            self.type = DATA

    def get_timestamp(self, frame):
        """Gets the time stamp of the frame"""
        try:
            timestr = frame[1:18].decode('cp1252')
            # ddmmyyyyhhmmss000
            day = int(timestr[0:2])
            month = int(timestr[2:4])
            year = int(timestr[4:8])
            hour = int(timestr[8:10])
            mins = int(timestr[10:12])
            sec = int(timestr[12:14])
            ms = int(timestr[14:17])
            return dt.datetime(year, month, day, hour, mins, sec, ms)
        except:
            return self.old_timestamp
