# vim:fileencoding=utf-8
# author: SaiChrla


def filelockread(addr, lock):
    """ Reads a file with apropriate lock"""
    file_name = '{}_{}.dat'.format(addr[0], str(addr[1]))
    with open(file_name, 'r', encoding='cp1252') as f:
        with lock:
            frame = f.read()
    return frame.encode('cp1252')


def filelockwrite(frame, addr, lock):
    """writes to a file to a file named after address with appropriate lock"""
    with open("{}_{}.dat".format(addr[0], str(addr[1])), 'w',
            encoding='cp1252') as f:
        with lock:
            f.write(frame.decode('cp1252'))


