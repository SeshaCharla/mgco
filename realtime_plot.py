#!vim: fileencoding=utf-8


import pickle
import matplotlib.pyplot as plt
import argparse as arg
import time


parser = arg.ArgumentParser()
parser.add_argument("htr", type=str , help="file name")
args = parser.parse_args()

htr = args.htr

with open('htrs.txt') as hl:
    hnames = hl.readlines()
hlist = [i[:-1] for i in hnames]
status = []
for i in hlist:
    status.append([])
t = []
while True:
    try:
        with open(htr, 'rb') as f:
            status = pickle.load(f)
    except:
        pass

    try:
        with open('t', 'rb') as f:
            t = pickle.load(f)
    except:
        pass
    plt.clf()
    plt.plot(t, status, label = htr)
    plt.legend()
    plt.pause(10)
    time.sleep(1)


plt.show()

