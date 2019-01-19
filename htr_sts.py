#!vim: fileencoding=utf-8


import protocol as p
import config
from multiprocessing import Lock
from filelockio import filelockread
import time
import datetime as dt
import pickle

def stat(sts):
    if sts == 'Htr-On  ':
        return 1
    elif sts == 'Htr-Off ':
        return 0
    else:
        return 0

n, addr_list, nparms_list, st_list = config.get_config()
lock = Lock()
frame = p.GCFrame(nparms_list[0])
with open('htrs.txt') as hl:
    hnames = hl.readlines()
hlist = [i[:-1] for i in hnames]
status = []
for i in hlist:
    status.append([])
try:
    for htr in hlist:
        with open(htr, 'rb') as f:
            status[hlist.index(htr)] = pickle.load(f)
except:
    pass

t = []
try:
    with open('t', 'rb') as f:
        t = pickle.load(f)
except:
    pass

while True:
    string  = filelockread(addr_list[0], lock)
    if frame.valid(p.Frame(string)):
        frame.update_frame(string)
        status_str = frame.data[(-13*8):].decode('cp1252')
        htr_sts = [status_str[8*i:8*(i+1)] for i in range(int(len(status_str)/8))]
        htr_sts_dict = dict(zip(hlist, htr_sts))
        print('\n \n')
        print(dt.datetime.now(),'\n')
        print("{:<15} {:<8}".format('Heater', 'Status'))
        t.append(dt.datetime.now())
        with open('t', 'wb') as ft:
            pickle.dump(t, ft)
        for htr, sts in htr_sts_dict.items():
            status[hlist.index(htr)].append(stat(sts))
            with open(htr, 'wb') as f:
                pickle.dump(status[hlist.index(htr)], f)
            print("{:<15} {:<8}".format(htr, sts))
        time.sleep(st_list[0])
    else:
        print('\n \n')
        print(dt.datetime.now())
        print('No Data! \n')
        time.sleep(st_list[0])

