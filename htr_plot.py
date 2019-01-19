#!vim: fileencoding=utf-8


import pickle
import matplotlib.pyplot as plt


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

for htr in hlist:
    i = hlist.index(htr)
    plt.figure(i)
    plt.plot(t, status[i], label = htr)
    plt.legend()

plt.show()
