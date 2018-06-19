# vim:fileencodeing=utf-8
# author: SaiChrla

import protocol as p
import datetime

file_name = '{}_{}.dat'.format(p.TEST_HOST, str(p.TEST_PORT))
with open(file_name, 'r', encoding='cp1252') as f:
    frame = f.read()
try:
    header = frame[:27]
    data = frame[27:]
    no_of_params = int(header[18:22])
    timestamp = datetime.datetime(header[5:9], header[3:5], header[1:3]
