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


