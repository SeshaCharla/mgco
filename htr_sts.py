#!vim: fileencoding=utf-8


import protocol as p
import config
from multiprocessing import Lock
from filelockio import filelockread
import time
import datetime as dt


n, addr_list, nparms_list, st_list = config.get_config()
lock = Lock()
string  = filelockread(addr_list[0], lock)
frame = p.GCFrame(nparms_list[0])
hnames = open('htrs.txt').readlines()
hlist = [i[:-1] for i in hnames]
while True:
    frame.update_frame(string)
    if frame.valid(p.Frame(string)):
        status_str = frame.data[(-14*8):].decode('cp1252')
        htr_sts = [status_str[8*i:8*(i+1)] for i in range(int(len(status_str)/8))]
        htr_sts_dict = dict(zip(hlist, htr_sts))
        print('\n \n')
        print(dt.datetime.now(),'\n')
        print("{:<15} {:<8}".format('Heater', 'Status'))
        for htr, sts in htr_sts_dict.items():
            print("{:<15} {:<8}".format(htr, sts))
        time.sleep(st_list[0])
    else:
        print('\n \n')
        print(dt.datetime.now())
        print('No Data! \n')
        time.sleep(st_list[0])

