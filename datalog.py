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
        return float(sts)

n, addr_list, nparms_list, st_list = config.get_config()
lock = Lock()
frame = p.GCFrame(nparms_list[0])
with open('names.txt') as nl:
    names = nl.readlines()
nlist = [i[:-1] for i in names]
status = []
for i in nlist:
    status.append([])
try:
    for token in nlist:
        with open('data/'+token, 'rb') as f:
            status[nlist.index(token)] = pickle.load(f)
except:
    pass

t = []
try:
    with open('data/t', 'rb') as f:
        t = pickle.load(f)
except:
    pass

while True:
    string  = filelockread(addr_list[0], lock)
    if frame.valid(p.Frame(string)):
        frame.update_frame(string)
        status_str = frame.data.decode('cp1252')
        token_sts = [status_str[8*i:8*(i+1)] for i in range(int(len(status_str)/8))]
        token_sts_dict = dict(zip(nlist, token_sts))
        t.append(dt.datetime.now())
        with open('data/t', 'wb') as ft:
            pickle.dump(t, ft)
        for token, sts in token_sts_dict.items():
            i = nlist.index(token)
            status[i].append(stat(sts))
            with open('data/'+token, 'wb') as f:
                pickle.dump(status[i], f)
        time.sleep(st_list[0])
    else:
        print('\n \n')
        print(dt.datetime.now())
        print('No Data! \n')
        time.sleep(st_list[0])

