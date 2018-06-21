# vim:fileencoding=utf-8
# author: SaiChrla


def readfile(addr):
    """ Reads the data file corresponding to the server"""
    file_name = '{}_{}.dat'.format(addr[0], str(addr[1]))
    with open(file_name, 'r', encoding='cp1252') as f:
        frame = f.read()
    return frame.encode('cp1252')


def filelockread(addr, lock):
    """ Reads a file with apropriate lock"""
    file_name = '{}_{}.dat'.format(addr[0], str(addr[1]))
    with open(file_name, 'r', encoding='cp1252') as f:
        with lock:
            frame = f.read()
    return frame.encode('cp1252')


