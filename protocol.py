# vim:fileencoding=utf-8
# AUthor: SaiChrla


""" This file has the necessary functions for reading and wrinting data in GCO
protocol. cp1252 encoding is used as '\xbb' and '\xcc' are represented by
corresponding hex nos. unlike utf-8 where is split in to 2 nos. """

import datetime as dt
import random as r


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


def get_frame(nparms):
    """ Randomly creats the frame"""
    s = lambda: '+'.encode('cp1252') if r.random()>0.5 else '-'.encode('cp1252')
    n = lambda: (str(round(75*r.random(), 2)).encode('cp1252')).rjust(7,
            '0'.encode('cp1252'))
    data = bytes()
    # if r.random() > 0.5:
    # for i in range(nparms):
      #   data = data + s() + n()
    header = creatheader(nparms, DATA)
    return STX + header + data + ETX


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

    def __init__(self, nparms):
        """Initial the gco-data object"""
        self.nparms = nparms
        self.invalid_data = self.nparms * bytes('+0000999', encoding='cp1252')
        self.old_timestamp = dt.datetime(2018, 4, 22)
        self.type = DATA
        self.data = bytes(''*nparms, encoding='cp1252')

    def update_frame(self, frame):
        """ update the gc-frame attributes """
        fr = Frame(frame)
        if self.valid(fr):
            self.data = fr.data
            self.type = fr.type
            self.old_timestamp = fr.timestamp

        else:
            self.set_invalid()


    def valid(self, fr):
        """ Returns the truth value of invalidity"""
        try:
            return ((fr.timestamp > self.old_timestamp) and self.crnprms())
        except:
            return False

    def set_invalid(self):
        """Makes the frame invalid"""
        self.data = self.invalid_data
        self.type = DATA


    def crnparms(self, fr):
        """ Check if the parms are same"""
        try:
            if fr.type:
                return len(fr.data)//8 == self.nparms
            else:
                return len(fr.data)//25 == self.nprms
        except:
            return False


class Frame:
    """ no nonsense frame class """
    # Frame details (Afterf stripping STX and ETX):
    # frame[0] = frame type (DATA, DB)
    # frame[1:18] = time stamp
    # frame[18:22] = no. of parms
    # frame[22:27] = white spaces
    # frame[27:] = data
    # if DATA: len = 8 bytes
    # if DB: len = 25 bytes


    def __init__(self, frame):
        """ Initiates the frame object with all the attributes"""
        self.type = get_type(frame)
        self.timestamp = get_timestamp(frame)
        self.data = get_data(frame)
        self.hnparms = get_hnparms(frame)


def get_timestamp(frame):
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
        return sdt.datetime(0, 0, 0, 0, 0, 0, 0)


def get_type(frame):
    """ set the type of frame"""
    try:
        d = frame[0]
        if d == DB_FRAME :
            ftype = DB
        else:
            ftype = DATA
    except:
        ftype = DATA
    return ftype


def get_data(frame):
    """ Get the data part of the frame"""
    try:
        return frame[27:]
    except:
        return bytes()

def get_hnparms(frame):
    """ returns the no. of parameters acc to haeders """
    try:
        return int(frame[18:22].decode('cp1252'))
    except:
        return 0
